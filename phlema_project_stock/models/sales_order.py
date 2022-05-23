from odoo import models, api


class StockSaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        conf = super(StockSaleOrder, self).action_confirm()
        if conf:
            stock_picking = self.env["stock.picking"]
            project = self.env["project.project"]

            location_id = (
                self.env["stock.picking.type"]
                .browse(self._context.get("default_picking_type_id"))
                .default_location_src_id
            )
            destination_id = (
                self.env["stock.picking.type"]
                .browse(self._context.get("default_picking_type_id"))
                .default_location_dest_id
            )
            for order in self:
                project_rec = order.project_id
                project_inst = project.search([("analytic_account_id", "=", int(project_rec.id))])
                # TODO: Filter by delivery status, ie only handle draft items
                if len(project_inst.project_delivery_ids) <= 0:
                    if order.project_items_ids and project_inst:
                        # Prepare job delivery
                        project_category_id = project_inst.project_categ_id
                        item_lst = []
                        for lst in order.project_items_ids:
                            item_lst.append(
                                (
                                    0,
                                    0,
                                    {
                                        "project_id": project_inst.id,
                                        "name": lst.name,
                                        "current_location_id": project_category_id.delivery_type_id.default_location_src_id.id,
                                        "project_item_id": lst.id,
                                        "product_id": lst.product_id.id,
                                        "product_uom": lst.product_uom_id.id,
                                    },
                                )
                            )
                        det_dev = {
                            "partner_id": order.partner_id.id,
                            "move_lines": item_lst,
                            "project_id": project_inst.id,
                            "location_id": project_inst.discharge_terminal_id.id
                            or project_category_id.delivery_type_id.default_location_src_id.id,
                            "location_dest_id": project_inst.discharge_terminal_id.id
                            or project_category_id.delivery_type_id.default_location_dest_id.id,
                            "picking_type_id": project_category_id.delivery_type_id.id,
                            "sale_id": order.id,
                            "has_delivery_process": True,
                       
                        }
                        pickings = stock_picking.create(det_dev)
                        if pickings:
                            picking_moves = pickings.mapped("move_lines")
                            for mv in picking_moves:
                                if mv.project_item_id:
                                    mv.project_item_id.write({"stock_move_id": mv.id})
        return conf
