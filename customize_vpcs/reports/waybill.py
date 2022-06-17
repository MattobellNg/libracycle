from tracemalloc import start
from odoo import models
from odoo.tools.misc import xlwt


class WaybillXlsx(models.AbstractModel):
    _name = 'report.customize_vpcs.report_waybill_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, items):
        print('Items :', items)
        headers = ["BL NO", "Job Ref No", "40FT", "20FT", "CBM", "KG", "ITEM DESCRIPTION", "SHIPPING LINE", "TERMINAL", "JOB DYNAMICS", "ATA", "TDO Date", "Delivery completion Date", "Final Destination", "Complete Doc. Received", "Duty", "Shipping charge", "Terminal Charge ", "NAFDAC",
                   "SON", "Agency", "Transportation", "Others", "Total Cost(N)", "Duty", "Shipping charge", "Terminal Charge ", "NAFDAC", "Agency", "Transportation", "Others", "Invoice Value(N)", "VAT(N)", "Total Invoice Value(N)", "Paid(N)", "WHT(N)", "Unpaid(N)", "Total Profit(N)", "COMMENT"]
        sheet = workbook.add_worksheet("waybill")
        cell_format = workbook.add_format(
            {"bold": True, "font_size": 8, "border": True, "align": 'left'})
        header_format = workbook.add_format(
            {"bold": True, "font_size": 8, "border": True, "align": 'center', })
        sheet.merge_range(
            0, 0, 0, 14, 'INVOICE SUBMISSION TRACKING REPORT - SPRINGFIELD AGRO', cell_format)
        sheet.merge_range(
            0, 15, 0, 23, 'EXPENSE CENTRES IN NAIRA(summation of inventory items in analytic/when amount double clicks it drills down to details/breakdown', cell_format)
        sheet.merge_range(0, 24, 0, 36, 'INVOICE CENTRES IN NAIRA/DOLLAR/EURO/POUNDS(summation of inventory items and all income lines in validated invoice reporting in analytic/when amount double clicks it drills down to details/breakdown', cell_format)
        sheet.merge_range(0, 37, 0, 38, 'Profile Section', cell_format)
        row = 1
        column = 0
        for i in headers:
            sheet.write(row,column,i,header_format)
            sheet.set_column(0,column,15)
            column+=1
        for item in items:
            pass