
from odoo import models, fields, api, _


class TripartiteReport(models.Model):

    _name = 'tripartite.report'
    _description = 'Tripartite Report'
    _sql_constraints = [
        ("name_unique", "unique(name)", "You can only have one record per customer"),
    ]

    name = fields.Many2one('res.partner', string='Customer')
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.uid)
    email = fields.Char('Email')
    attachment_ids = fields.Many2many('ir.attachment', string='Report')

    @api.onchange('name')
    def _onchange_name(self):
        if self.name:
            return {'value': {
                'email': self.name.email
            }}

    @api.model
    def _cron_run_tripartite_report(self):
        "CRON to send report with an attachment"
        activity_reports = self.search([])
        for activity_report in activity_reports:
            email_template = self.env.ref(
                'libra_periodic_reports.tripartite_report_template')
            email_template.attachment_ids = [
                (6, _, [activity_report.attachment_ids[-1].id])]
            email_template.send_mail(activity_report.id)
            email_template.attachment_ids = [(5, 0, 0)]
        return True
