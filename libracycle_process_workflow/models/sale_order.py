from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    name = fields.Char(string='Invoice Number', required=True, copy=False, readonly=True, states={'draft': [('readonly', False)]}, index=True)

    @api.model
    def create(self, vals):
        name = vals.get('name')
        if not name:
            seq_date = fields.Datetime.context_timestamp(self, fields.Datetime.now())
            vals['name'] = self.env['ir.sequence'].next_by_code('lbc.invoice.number', sequence_date=seq_date)
        return super(SaleOrder, self).create(vals)


   