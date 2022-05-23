from odoo import fields, models, api, _
from odoo.addons import decimal_precision as dp


class PackOperationMovement(models.Model):
    _name = "stock.pack.sub.operation"

    location_id = fields.Many2one("stock.location", "Source Location", required=True)
    location_dest_id = fields.Many2one("stock.location", "Destination Location", required=True)
    operation_id = fields.Many2one("stock.pack.operation", "Ralated Pack Operations")

    stock_move_id = fields.Many2one("stock.move", "Item")


class PackOperation(models.Model):
    _inherit = "stock.move.operation"

    in_transit_done = fields.Float(
        "In Transit Done",
        default=0.0,
        digits=dp.get_precision("Product Unit of Measure"),
    )

    operation_move_id = fields.One2many("stock.pack.sub.operation", "operation_id", "Sub Operation Move")

    move_operation_ids = fields.Many2many(
        "stock.move",
        string="Ready for Move",
        domain="[('current_location_id', '=', location_id), ('picking_id', '=', picking_id), ('product_id', '=', product_id),('state', '=', 'assigned'), ('delivery_status', 'in', ['draft', 'prepare', 'dispatch', 'in_transit'])]",
    )


    @api.onchange("move_operation_ids")
    def update_qty_to_process(self):
        if self.move_operation_ids:
            if self.location_dest_id.usage != "customer":
                self.in_transit_done = len(self.move_operation_ids)
                self.product_qty -= self.in_transit_done
            else:
                self.qty_done = len(self.move_operation_ids)

    def get_sub_operation(self, operation_id, move_id, loc_id, loc_dest_id):
        return {
            "stock_move_id": move_id,
            "operation_id": operation_id,
            "location_id": loc_id,
            "location_dest_id": loc_dest_id,
        }

    def write(self, vals):
        its_customer_dest = True
        new_operation = False
        if self.picking_id.has_delivery_process:
            dest_location_id = vals.get("location_dest_id", self.location_dest_id.id)
            location_id = vals.get("location_id", self.location_id.id)
            if dest_location_id:
                location_det = self.env["stock.location"].browse(int(dest_location_id))
                if location_det and location_det.usage != "customer":
                    if vals.get("in_transit_done") <= 0.0:
                        vals["in_transit_done"] = vals.get("qty_done")
                        vals["qty_done"] = 0.0
                    its_customer_dest = False
            qty_done = vals.get("qty_done", 0)
            if qty_done > 0.0 and not vals.get("move_operation_ids"):
                move_ids = []
                if self.location_dest_id.usage != "customer":
                    vals.get["in_transit_done"] = vals.get("qty_done")
                get_picking_moves = self.env["stock.move"].search(
                    [
                        ("picking_id", "=", self.picking_id.id),
                        ("product_id", "=", self.product_id),
                        ("current_location_id", "=", dest_location_id),
                        ("delivery_status", "in", ["draft", "prepare"]),
                    ]
                )
                if get_picking_moves:
                    xy = 0
                    for pick_move in get_picking_moves:
                        if xy > vals.get("qty_done"):
                            continue
                        move_ids.append(pick_move.id)
                        xy += 1
                if move_ids:
                    vals["move_operation_ids"] = [(6, 0, move_ids)]
            if not its_customer_dest and vals.get("move_operation_ids") and vals.get("in_transit_done") > 0.0:
                in_transit = vals.get("in_transit_done", self.in_transit_done)
                get_old_operation = self.env["stock.pack.operation"].search(
                    [
                        ("product_id", "=", self.product_id.id),
                        ("location_id", "=", location_id),
                        ("location_dest_id", "=", dest_location_id),
                    ],
                    limit=1,
                )
                if get_old_operation:
                    to_do_items = in_transit + get_old_operation.product_qty
                    new_operation = get_old_operation
                    get_old_operation.write({"in_transit_done": to_do_items, "product_qty": to_do_items})

                else:
                    new_operation = self.copy(
                        {
                            "qty_done": 0.0,
                            "in_transit_done": 0.00,
                            "location_id": location_id,
                            "location_dest_id": dest_location_id,
                            "product_qty": in_transit,
                            "move_operation_ids": False,
                            "operation_move_id": False,
                        }
                    )
                if new_operation:
                    if vals.get("location_id"):
                        vals.pop("location_id")
                    if vals.get("location_dest_id"):
                        vals.pop("location_dest_id")
                    pro_qty = vals.get("product_qty", self.product_qty)
                    vals["product_qty"] = pro_qty - in_transit if pro_qty > 0 else 0
                    vals["qty_done"] = 0.00
                    vals["in_transit_done"] = 0.0
                    # vals['move_operation_ids'] = False
            # Update transaction history and stock.move location
            if vals.get("move_operation_ids"):
                move_ids = vals.get("move_operation_ids")
                if move_ids:
                    sub_ops_rec = []
                    opera_id = new_operation.id if new_operation else self.id
                    for x, y, ids in move_ids:
                        for rec in ids:
                            # Get stock Move rec
                            move_rec = self.env["stock.move"].browse(rec)
                            if move_rec:
                                state = "in_transit" if vals.get("in_transit_done") > 0 else "dispatch"
                                move_rec.write(
                                    {
                                        "current_location_id": dest_location_id,
                                        "delivery_status": state,
                                    }
                                )
                            data = self.get_sub_operation(opera_id, rec, location_id, dest_location_id)
                            sub_ops_rec.append((0, 0, data))
                    vals["operation_move_id"] = sub_ops_rec
                    if not its_customer_dest:
                        vals["move_operation_ids"] = False

        return super(PackOperation, self).write(vals)


class StockMoveOperationLinkInherit(models.Model):
    _inherit = "stock.move.operation.link"
    _rec_name = "item_code"

    item_size = fields.Float("Size", related="move_id.item_size")
    item_code = fields.Char("Item Code", related="move_id.name")
    product_uom_id = fields.Many2one("uom.uom", "Unit of Measure", related="move_id.product_uom_id")

    def add_move(self):
        self.processed_flg = True
        pass

    def remove_move(self):
        self.processed_flg = False
        return False
