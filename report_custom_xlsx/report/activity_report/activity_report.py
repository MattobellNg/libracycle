import logging
from odoo import models

from ...constants import ACTIVITY_REPORT_HEADERS


class PartnerXlsx(models.AbstractModel):
    _name = 'report.report_custom_xlsx.activity_report'
    _description = 'Activity report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        sheet = workbook.add_worksheet("Activity report sheet")
        header_format = workbook.add_format({'bold': True, 'bg_color': '#cfcfcf', 'border': 1, 'border_color': '#383838'})
        report_format = workbook.add_format({'border': 1, 'border_color': '#383838'})
        sheet.write(0, 4, f'25th March, 2024 Activity Report for {partners.name}')
        row, col = 1, 1
        contents = data.get("contents")
        for header in data.get("headers"):
            sheet.write('B%d' % (row + 1), (header.replace("_", " ")).capitalize())
            row += 1
            sheet.write_row(row, col, data.get('headers')[header], header_format)
            row += 1
            row_data = contents.get(f"{(header.lower()).replace('_', '.')}", None) # returns a list
            if row_data is None:
                continue
            count = 1
            for r in row_data:
                sheet.write(row, col, count, report_format)
                col += 1
                for val in r:
                    sheet.write(row, col, r[val], report_format)
                    col += 1
                col = 1
                row += 1
                count += 1
            col = 1
            row += 1


