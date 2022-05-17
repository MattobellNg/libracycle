from odoo import fields, models, api


class ResPartnerExtension(models.Model):
    _inherit = "res.partner"

    is_delivery_partner = fields.Boolean("Delivery Person/Company", default=False)
