from odoo import fields, models, api


class StockMoveExtension(models.Model):
    _inherit = "stock.move"

    project_item_id = fields.Many2one("project.schedule.items", "Job Item")
    item_size = fields.Float("Size", related="project_item_id.size")
    item_code = fields.Char("Item Code", related="project_item_id.name")
    product_uom_id = fields.Many2one("uom.uom", "Unit of Measure", related="project_item_id.product_uom_id")
    project_id = fields.Many2one("project.project", "Project")

    current_location_id = fields.Many2one("stock.location", "Current Location", required=True)

    delivery_partner_id = fields.Many2one(
        "res.partner", "Delivery Person", domain="[('is_delivery_partner', '=', True)]"
    )
    delivery_partner_name = fields.Char("Delivery Person Name")
    delivery_partner_phone = fields.Char("Delivery Phone Number")

    delivery_status = fields.Selection(
        [
            ("draft", "Draft"),
            ("prepare", "Prepared"),
            ("in_transit", "In Transit"),
            ("dispatch", "Dispatched"),
            ("delivered", "Delivered"),
        ],
        "Delivery Status",
        default="draft",
    )

    def write(self, vals):
        if vals.get("state") == "done" and vals.get("date"):
            vals["delivery_status"] = "dispatch"
        elif vals.get("state") in ["assigned", "confirmed"]:
            vals["delivery_status"] = "prepare"
        res = super(StockMoveExtension, self).write(vals)
        if res:
            for move in self:
                if move.project_id and vals.get("state") == "done":
                    move.project_id.action_delivered()
