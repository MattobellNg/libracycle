from odoo import fields, models, api


class AccountInvoiceExt(models.Model):
    _inherit = "account.move"

    def _default_job_id(self):
        job_id = False
        if self._context.get("job_id") or self._context.get("default_job_id"):
            job_id = self._context.get("job_id") or self._context.get("default_job_id")
        return job_id

    job_id = fields.Many2one("project.project", "Job ID", default=_default_job_id)


class AccountInvoiceLine(models.Model):
    _inherit = "account.move.line"

    @api.onchange("product_id")
    def _onchange_product_id(self):
        res = super(AccountInvoiceLine, self)._onchange_product_id()

        if self.invoice_id.job_id and self.product_id:
            self.account_analytic_id = self.invoice_id.job_id.analytic_account_id.id

        return res
