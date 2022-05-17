from odoo import fields, models, api, _
from odoo.tools.float_utils import float_compare


class StockPickingExtension(models.Model):
    _inherit = "stock.picking"

    project_id = fields.Many2one("project.project", "Job ID")
    has_delivery_process = fields.Boolean("Delivery Process", default=False)

    def action_prep_delivery(self):
        pass

    def recompute_remaining_qty(self, done_qtys=False):

        selected_moves = self.pack_operation_ids.mapped("move_operation_ids")

        def _create_link_for_index(operation_id, index, product_id, qty_to_assign, quant_id=False):
            move_dict = prod2move_ids[product_id][index]
            x_move_dict = move_dict["move"]
            qty_on_link = min(move_dict["remaining_qty"], qty_to_assign)
            if self.has_delivery_process:
                if x_move_dict in selected_moves:
                    self.env["stock.move.operation.link"].create(
                        {
                            "move_id": move_dict["move"].id,
                            "operation_id": operation_id,
                            "qty": qty_on_link,
                            "reserved_quant_id": quant_id,
                        }
                    )
                    if move_dict["remaining_qty"] == qty_on_link:
                        prod2move_ids[product_id].pop(index)
                    else:
                        move_dict["remaining_qty"] -= qty_on_link
                else:
                    qty_on_link = 0.0
            else:
                self.env["stock.move.operation.link"].create(
                    {
                        "move_id": move_dict["move"].id,
                        "operation_id": operation_id,
                        "qty": qty_on_link,
                        "reserved_quant_id": quant_id,
                    }
                )
                if move_dict["remaining_qty"] == qty_on_link:
                    prod2move_ids[product_id].pop(index)
                else:
                    move_dict["remaining_qty"] -= qty_on_link

            return qty_on_link

        def _create_link_for_quant(operation_id, quant, qty):
            """create a link for given operation and reserved move of given quant, for the max quantity possible, and returns this quantity"""
            if not quant.reservation_id.id:
                return _create_link_for_product(operation_id, quant.product_id.id, qty)
            qty_on_link = 0
            for i in range(0, len(prod2move_ids[quant.product_id.id])):
                if prod2move_ids[quant.product_id.id][i]["move"].id != quant.reservation_id.id:
                    continue
                qty_on_link = _create_link_for_index(operation_id, i, quant.product_id.id, qty, quant_id=quant.id)
                break
            return qty_on_link

        def _create_link_for_product(operation_id, product_id, qty):
            """method that creates the link between a given operation and move(s) of given product, for the given quantity.
            Returns True if it was possible to create links for the requested quantity (False if there was not enough quantity on stock moves)"""
            qty_to_assign = qty
            Product = self.env["product.product"]
            product = Product.browse(product_id)
            rounding = uom.uom_id.rounding
            qtyassign_cmp = float_compare(qty_to_assign, 0.0, precision_rounding=rounding)
            if prod2move_ids.get(product_id):
                vy = 0
                while prod2move_ids[product_id] and qtyassign_cmp > 0:
                    if self.has_delivery_process:
                        if len(prod2move_ids[product_id]) == vy:
                            break
                        qty_on_link = _create_link_for_index(
                            operation_id, vy, product_id, qty_to_assign, quant_id=False
                        )
                        qty_to_assign -= qty_on_link
                        qtyassign_cmp = float_compare(qty_to_assign, 0.0, precision_rounding=rounding)
                        if len(prod2move_ids[product_id]) <= vy:
                            qtyassign_cmp = 0
                        vy += 1
                        if qty_on_link > 0.0:
                            vy -= int(qty_on_link)
                    else:
                        qty_on_link = _create_link_for_index(operation_id, 0, product_id, qty_to_assign, quant_id=False)
                        qty_to_assign -= qty_on_link
                        qtyassign_cmp = float_compare(qty_to_assign, 0.0, precision_rounding=rounding)

            return qtyassign_cmp == 0

        # TDE CLEANME: oh dear ...
        Uom = self.env["uom.uom"]
        QuantPackage = self.env["stock.quant.package"]
        OperationLink = self.env["stock.move.operation.link"]

        quants_in_package_done = set()
        prod2move_ids = {}
        still_to_do = []
        # make a dictionary giving for each product, the moves and related quantity that can be used in operation links
        moves = sorted(
            [x for x in self.move_lines if x.state not in ("done", "cancel")],
            key=lambda x: (((x.state == "assigned") and -2 or 0) + (x.partially_available and -1 or 0)),
        )
        for move in moves:
            if not prod2move_ids.get(move.product_id.id):
                prod2move_ids[move.product_id.id] = [{"move": move, "remaining_qty": move.product_qty}]
            else:
                prod2move_ids[move.product_id.id].append({"move": move, "remaining_qty": move.product_qty})

        need_rereserve = False
        # sort the operations in order to give higher priority to those with a package, then a lot/serial number
        operations = self.pack_operation_ids
        operations = sorted(
            operations,
            key=lambda x: ((x.package_id and not x.product_id) and -4 or 0)
            + (x.package_id and -2 or 0)
            + (x.pack_lot_ids and -1 or 0),
        )
        # delete existing operations to start again from scratch
        links = OperationLink.search([("operation_id", "in", [x.id for x in operations])])
        if links:
            links.unlink()
        # 1) first, try to create links when quants can be identified without any doubt
        for ops in operations:
            lot_qty = {}
            for packlot in ops.pack_lot_ids:
                lot_qty[packlot.lot_id.id] = ops.product_uom_id._compute_quantity(packlot.qty, ops.product_id.uom_id)
            # for each operation, create the links with the stock move by seeking on the matching reserved quants,
            # and deffer the operation if there is some ambiguity on the move to select
            if ops.package_id and not ops.product_id and (not done_qtys or ops.qty_done):
                # entire package
                for quant in ops.package_id.get_content():
                    remaining_qty_on_quant = quant.qty
                    if quant.reservation_id:
                        # avoid quants being counted twice
                        quants_in_package_done.add(quant.id)
                        qty_on_link = _create_link_for_quant(ops.id, quant, quant.qty)
                        remaining_qty_on_quant -= qty_on_link
                    if remaining_qty_on_quant:
                        still_to_do.append((ops, quant.product_id.id, remaining_qty_on_quant))
                        need_rereserve = True
            elif ops.product_id.id:
                # Check moves with same product
                product_qty = ops.qty_done if done_qtys else ops.product_qty
                qty_to_assign = ops.product_uom_id._compute_quantity(product_qty, ops.product_id.uom_id)
                precision_rounding = ops.product_id.uom_id.rounding
                for move_dict in prod2move_ids.get(ops.product_id.id, []):
                    move = move_dict["move"]
                    for quant in move.reserved_quant_ids:
                        if float_compare(qty_to_assign, 0, precision_rounding=precision_rounding) != 1:
                            break
                        if quant.id in quants_in_package_done:
                            continue

                        # check if the quant is matching the operation details
                        if ops.package_id:
                            flag = quant.package_id == ops.package_id
                        else:
                            flag = not quant.package_id.id
                        flag = flag and (ops.owner_id.id == quant.owner_id.id)
                        if flag:
                            if not lot_qty:
                                max_qty_on_link = min(quant.qty, qty_to_assign)
                                qty_on_link = _create_link_for_quant(ops.id, quant, max_qty_on_link)
                                qty_to_assign -= qty_on_link
                            else:
                                if lot_qty.get(quant.lot_id.id):  # if there is still some qty left
                                    max_qty_on_link = min(
                                        quant.qty,
                                        qty_to_assign,
                                        lot_qty[quant.lot_id.id],
                                    )
                                    qty_on_link = _create_link_for_quant(ops.id, quant, max_qty_on_link)
                                    qty_to_assign -= qty_on_link
                                    lot_qty[quant.lot_id.id] -= qty_on_link

                qty_assign_cmp = float_compare(qty_to_assign, 0, precision_rounding=precision_rounding)
                if qty_assign_cmp > 0:
                    # qty reserved is less than qty put in operations. We need to create a link but it's deferred after we processed
                    # all the quants (because they leave no choice on their related move and needs to be processed with higher priority)
                    still_to_do += [(ops, ops.product_id.id, qty_to_assign)]
                    need_rereserve = True

        # 2) then, process the remaining part
        all_op_processed = True
        for ops, product_id, remaining_qty in still_to_do:
            all_op_processed = _create_link_for_product(ops.id, product_id, remaining_qty) and all_op_processed
        return (need_rereserve, all_op_processed)
