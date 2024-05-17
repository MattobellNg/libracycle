import logging
from odoo import models
_logger = logging.getLogger(__name__)

class MicrodailyXlsx(models.AbstractModel):
    _name = 'report.report_custom_xlsx.microdaily_report'
    _description = 'Microdaily report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        sheet = workbook.add_worksheet("Microdaily report sheet")
        cell_format = workbook.add_format({'border': 1, 'border_color': '#383838'})
        blue_header_format = workbook.add_format({'bold': True, 'bg_color': '#05c5fa', 'border': 1, 'border_color': '#383838'})
        yellow_header_format = workbook.add_format({'bold': True, 'bg_color': 'yellow', 'border': 1, 'border_color': '#383838'})
        sheet.write_row('A2', data.get("headers"), blue_header_format)
        row, col = 2, 0
        for r in data.get('microdaily_report_ids'):
            col = 0
            for k in r.keys():
                sheet.write(row, col, r[k], cell_format)
                col +=1
            row += 1
        return sheet

