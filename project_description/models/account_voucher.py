from odoo import fields, models, api


class AccountVoucherExtend(models.Model):
    _inherit = "account.voucher"

    def _default_job_id(self):
        job_id = False
        if self._context.get("job_id") or self._context.get("default_job_id"):
            job_id = self._context.get("job_id") or self._context.get("default_job_id")
        return job_id

    job_id = fields.Many2one("project.project", "Job ID", default=_default_job_id)


class AccountVoucherLineExtend(models.Model):
    _inherit = "account.voucher.line"

    def product_id_change(
        self,
        product_id,
        partner_id=False,
        price_unit=False,
        company_id=None,
        currency_id=None,
        type=None,
    ):
        res = super(AccountVoucherLineExtend, self).product_id_change(
            product_id, partner_id, price_unit, company_id, currency_id, type
        )
        if res and self.voucher_id.job_id and product_id:
            res["value"]["account_analytic_id"] = self.voucher_id.job_id.analytic_account_id.id
        return res
