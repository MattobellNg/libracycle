from odoo import api, fields, models


class HrExpenseSheet(models.Model):
    _inherit = "hr.expense.sheet"

    journal_balance = fields.Float(
        string="Account Balance", compute="_compute_journal_balance"
    )

    @api.depends("journal_id")
    def _compute_journal_balance(self):
        for rec in self:
            rec.journal_balance = rec.journal_id.default_account_id.current_balance
