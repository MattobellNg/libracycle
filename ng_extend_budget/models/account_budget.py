from odoo import api, fields, models

class CrossoveredBudgetLines(models.Model):
    _inherit = "crossovered.budget.lines"

    budget_variance = fields.Monetary(
        string='Budget Variance',
        compute='_compute_budget_variance',
        store=True,
        readonly=True,
        force_save=1,
    )

    @api.depends('theoretical_amount', 'practical_amount')
    def _compute_budget_variance(self):
        for line in self:
            line.budget_variance = line.theoritical_amount - line.practical_amount