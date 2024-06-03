# -*- coding: utf-8 -*-
from collections import defaultdict
import logging
import base64
from odoo import models, api, _, SUPERUSER_ID
from ..constants import TRIPARTITE_REPORT_HEADER, MICRO_DAILY_REPORT_HEADER, MONTHLY_INVOICING_REPORT_HEADER, ACTIVITY_REPORT_HEADERS

serial_no = 1

def get_records_by_partner(cr, partner_id):
    records_by_model = defaultdict(list)
    env = api.Environment(cr, SUPERUSER_ID, {})
    # List of all models to consider
    models_to_check = [
        'quotation.await.approval',
        'awaiting.shipment',
        'awaiting.arrival',
        'arrived.in.clearing',
        'delivered.not.invoiced',
        'activity.invoicing'
    ]

    # Iterate over each model to retrieve records
    for model in models_to_check:
        Model = env[model]
        records = Model.search([('name', '=', partner_id.id)])
        for record in records:
            records_by_model[Model._name].append(Model.get_report_data(record))
    return records_by_model

class ResPartner(models.Model):
    _inherit = 'res.partner'

    def _cron_run_tripartite_report(self):
        "CRON to send report with an attachment"
        partners_with_tripartite_report = self.env['tripartite.report'].sudo().search([
        ]).mapped('name')
        for partner in partners_with_tripartite_report:
            partner._send_tripartite_report_email()
        return True

    def _send_tripartite_report_email(self):
        TripartiteReport = self.env['tripartite.report'].sudo()
        report = self.env.ref('report_custom_xlsx.tripartite_report_xlsx')
        tripartite_report_ids = TripartiteReport.search(
            [('name', '=', self.id)])
        tripartite_report_ids = [TripartiteReport.get_report_data(
            rep) for rep in tripartite_report_ids]
        for tripartite_report in tripartite_report_ids:
            global serial_no
            tripartite_report.update(serial_no=serial_no)
            serial_no += 1
        data = {
            'context': self.env.context.copy(),
            'headers': TRIPARTITE_REPORT_HEADER,
            'tripartite_report_ids': tripartite_report_ids,
        }
        generated_report = report._render_xlsx(self.id, data=data)
        data_record = base64.b64encode(generated_report[0])
        ir_values = {
            'name': 'Tripartite Report.xlsx',
            'type': 'binary',
            'datas': data_record,
            'store_fname': data_record,
            'mimetype': 'application/vnd.ms-excel',
            'res_model': 'res.partner',
        }
        attachment = self.env['ir.attachment'].sudo().create(ir_values)
        email_template = self.env.ref(
            'report_custom_xlsx.tripartite_report_template')
        email_template.attachment_ids = [(6, _, [attachment.id])]
        email_template.send_mail(self.id)
        email_template.attachment_ids = [(5, 0, 0)]
        return True

    def _cron_run_microdaily_report(self):
        "CRON to send report with an attachment"
        partners_with_microdaily_report = self.env['microdaily.report'].sudo().search([
        ]).filtered(lambda md: md.report_file).mapped('name')
        for partner in partners_with_microdaily_report:
            partner._send_microdaily_report_email()
        return True

    def _send_microdaily_report_email(self):
        """Microdaily report to be sent to individual customers"""
        MicrodailyReport = self.env['microdaily.report'].sudo()
        microdaily_report = MicrodailyReport.search(
            [('name', '=', self.id)]).filtered(lambda r: r.report_file)
        data_record = base64.b64decode(base64.b64encode(microdaily_report.report_file))
        ir_values = {
            'name': 'Microdaily Report.pdf',
            'type': 'binary',
            'datas': data_record,
            'store_fname': data_record,
            'mimetype': 'application/pdf',
            'res_model': 'res.partner',
        }
        attachment = self.env['ir.attachment'].sudo().create(ir_values)
        email_template = self.env.ref(
            'report_custom_xlsx.microdaily_report_template')
        email_template.attachment_ids = [(6, _, [attachment.id])]
        email_template.send_mail(self.id)
        email_template.attachment_ids = [(5, 0, 0)]
        return True
    
    # def _send_microdaily_report_email(self):
    #     """Microdaily report to be sent to individual customers"""
    #     MicrodailyReport = self.env['microdaily.report'].sudo()
    #     report = self.env.ref('report_custom_xlsx.microdaily_report_xlsx')
    #     microdaily_report_ids = MicrodailyReport.search(
    #         [('name', '=', self.id)])
    #     microdaily_report_ids = [MicrodailyReport.get_report_data(
    #         rep) for rep in microdaily_report_ids]
    #     data = {
    #         'context': self.env.context.copy(),
    #         'headers': MICRO_DAILY_REPORT_HEADER,
    #         'microdaily_report_ids': microdaily_report_ids,
    #     }
    #     report = self.env.ref('report_custom_xlsx.microdaily_report_xlsx')
    #     generated_report = report._render_xlsx(self.id, data=data)
    #     data_record = base64.b64encode(generated_report[0])
    #     ir_values = {
    #         'name': 'Microdaily Report.xlsx',
    #         'type': 'binary',
    #         'datas': data_record,
    #         'store_fname': data_record,
    #         'mimetype': 'application/vnd.ms-excel',
    #         'res_model': 'res.partner',
    #     }
    #     attachment = self.env['ir.attachment'].sudo().create(ir_values)
    #     email_template = self.env.ref(
    #         'report_custom_xlsx.microdaily_report_template')
    #     email_template.attachment_ids = [(6, _, [attachment.id])]
    #     email_template.send_mail(self.id)
    #     email_template.attachment_ids = [(5, 0, 0)]
    #     return True

    def _cron_run_monthly_invoicing_report(self):
        "CRON to send report with an attachment"
        partners_with_monthly_invoicing_report = self.env['monthly_invoicing.report'].sudo(
        ).search([]).mapped('name')
        for partner in partners_with_monthly_invoicing_report:
            partner._send_monthly_invoicing_report_email()
        return True

    def _send_monthly_invoicing_report_email(self):
        MonthlyInvoicingReport = self.env['monthly_invoicing.report'].sudo()
        report = self.env.ref('report_custom_xlsx.monthly_invoicing_report_xlsx')
        monthly_invoicing_report_ids = MonthlyInvoicingReport.search(
            [('name', '=', self.id)])
        monthly_invoicing_report_ids = [MonthlyInvoicingReport.get_report_data(
            rep) for rep in monthly_invoicing_report_ids]
        data = {
            'context': self.env.context.copy(),
            'headers': MONTHLY_INVOICING_REPORT_HEADER,
            'monthly_invoicing_report_ids': monthly_invoicing_report_ids,
        }
        report = self.env.ref(
            'report_custom_xlsx.monthly_invoicing_report_xlsx')
        generated_report = report._render_xlsx(
            self.id, data=data)
        data_record = base64.b64encode(generated_report[0])
        ir_values = {
            'name': 'Monthly Invoicing Report.xlsx',
            'type': 'binary',
            'datas': data_record,
            'store_fname': data_record,
            'mimetype': 'application/vnd.ms-excel',
            'res_model': 'res.partner',
        }
        attachment = self.env['ir.attachment'].sudo().create(ir_values)
        email_template = self.env.ref(
            'report_custom_xlsx.monthly_invoicing_report_template')
        email_template.attachment_ids = [(6, _, [attachment.id])]
        email_template.send_mail(self.id)
        email_template.attachment_ids = [(5, 0, 0)]
        return True

    def _cron_run_activity_report(self):
        "CRON to send report with an attachment"
        partners_with_activity_report = self.env['quotation.await.approval'].sudo(
        ).search([]).mapped('name')
        for partner in partners_with_activity_report:
            partner._send_activity_report_email(partner_data=get_records_by_partner(self._cr, partner))       
        return True

    def _send_activity_report_email(self, partner_data):
        data = {
            'context': self.env.context.copy(),
            'headers': ACTIVITY_REPORT_HEADERS,
            'contents': partner_data,
        }
        report = self.env.ref('report_custom_xlsx.activity_report_xlsx')
        generated_report = report._render_xlsx(self.id, data)
        data_record = base64.b64encode(generated_report[0])
        ir_values = {
            'name': 'Activity Report.xlsx',
            'type': 'binary',
            'datas': data_record,
            'store_fname': data_record,
            'mimetype': 'application/vnd.ms-excel',
            'res_model': 'res.partner',
        }
        attachment = self.env['ir.attachment'].sudo().create(ir_values)
        email_template = self.env.ref(
            'report_custom_xlsx.activity_report_template')
        email_template.attachment_ids = [(6, _, [attachment.id])]
        email_template.send_mail(self.id)
        email_template.attachment_ids = [(5, 0, 0)]
        return True
