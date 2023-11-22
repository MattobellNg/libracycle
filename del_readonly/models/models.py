# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = "account.move"
    invoice_date = fields.Date(string='Invoice/Bill Date', index=True, copy=False)
    x_studio_qac_reviewed=fields.Boolean("QAC Reviewed")

    def action_qac_approve(self):
        for rec in self:
            rec.broadcast_notification_officer()
            rec.write({'state': 'officer',
                       'x_studio_qac_reviewed':True})