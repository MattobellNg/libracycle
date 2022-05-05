from odoo import fields, models, api, _


class ProjectCategoryExtended(models.Model):
    _inherit = "project.project.category"

    delivery_type_id = fields.Many2one("stock.picking.type", "Delivery Type", required=True)
