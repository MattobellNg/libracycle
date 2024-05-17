import logging
from odoo import models

class PartnerXlsx(models.AbstractModel):
    _name = 'report.report_custom_xlsx.monthly_invoicing_report'
    _description = 'Monthly Invoicing report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        sheet = workbook.add_worksheet("Monthly Invoicing report sheet")
        format_underline = workbook.add_format({'underline': 1})
        cell_format = workbook.add_format({'border': 1, 'border_color': '#383838'})
        blue_header_format = workbook.add_format({'bold': True, 'bg_color': '#02fa07', 'border': 1, 'border_color': '#383838'})
        sheet.write('A1', 'Monthly Report', format_underline)
        sheet.write_row('A2', data.get("headers"), blue_header_format)
        row, col = 2, 0
        for r in data.get('monthly_invoicing_report_ids'):
            col = 0
            for k in r.keys():
                sheet.write(row, col, r[k], cell_format)
                col +=1
            row += 1
        return sheet

