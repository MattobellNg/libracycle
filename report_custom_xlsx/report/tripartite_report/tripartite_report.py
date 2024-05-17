import logging
from odoo import models


class PartnerXlsx(models.AbstractModel):
    _name = 'report.report_custom_xlsx.tripartite_report'
    _description = 'Tripartite report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        sheet = workbook.add_worksheet("Tripartite report sheet")
        header_format = workbook.add_format({'bold': True, 'bg_color': '#d9bfb0', 'border': 1, 'border_color': '#383838'})
        report_format = workbook.add_format({'border': 1, 'border_color': '#383838'})
        note_format = workbook.add_format({"bold": True})
        report_data = data.get('tripartite_report_ids')
        sheet.write_row('A2', data.get('headers'), header_format)
        row, col = 2, 0
        for r in report_data:
            col = 0
            for k in r.keys():
                sheet.write(row, col, r[k], report_format)
                col +=1
            row += 1
        row += 2
        col = 0
        sheet.write(row, col, 'Cummulative report', note_format)
        row += 1
        sheet.write(row, col, 'Report is done by bank on different sheet.', note_format)
        return sheet

