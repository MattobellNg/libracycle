import base64
import io
from odoo import models


class ProjectAccountReportXlsx(models.AbstractModel):
    _name = "report.vpcs_project_report_xlsx.project_account_report_template"
    _inherit = "report.report_xlsx.abstract"

    def generate_xlsx_report(self, workbook, data, project):
        sheet = workbook.add_worksheet("Report")
        bold = workbook.add_format({"bold": True})
        row = 0
        col = 0

        sheet.write(row, col, "Label", bold)
        sheet.write(row, col + 1, "Date", bold)
        sheet.write(row, col + 2, "Journal Entry", bold)
        sheet.write(row, col + 3, "Account", bold)
        sheet.write(row, col + 4, "Label", bold)
        sheet.write(row, col + 5, "Amount In Currency", bold)
        sheet.write(row, col + 6, "Debit", bold)
        sheet.write(row, col + 7, "credit", bold)
        sheet.write(row, col + 8, "Matching", bold)

        if data.get("Duty"):
            for i in data.get("Duty"):
                row += 1
                sheet.write(row, col, "Duty", bold)
                if i.get("date"):
                    sheet.write(row, col + 1, i.get("date"), bold)
                if i.get("move_id"):
                    sheet.write(row, col + 2, str(i.get("move_id")), bold)
                if i.get("account_id"):
                    sheet.write(row, col + 3, str(i.get("account_id")), bold)
                if i.get("name"):
                    sheet.write(row, col + 4, str(i.get("name")), bold)
                sheet.write(row, col + 5, str(i.get("amount_currency")), bold)
                sheet.write(row, col + 6, str(i.get("debit")), bold)
                sheet.write(row, col + 7, str(i.get("credit")), bold)
                if i.get("matching_number"):
                    sheet.write(row, col + 8, str(i.get("matching_number")), bold)

        rowTerminal = row
        if data.get("Terminal"):
            for i in data.get("Terminal"):
                rowTerminal += 1
                sheet.write(rowTerminal, col, "Terminal", bold)
                if i.get("date"):
                    sheet.write(rowTerminal, col + 1, i.get("date"), bold)
                if i.get("move_id"):
                    sheet.write(rowTerminal, col + 2, str(i.get("move_id")), bold)
                if i.get("account_id"):
                    sheet.write(rowTerminal, col + 3, str(i.get("account_id")), bold)
                if i.get("name"):
                    sheet.write(rowTerminal, col + 4, str(i.get("name")), bold)
                sheet.write(rowTerminal, col + 5, str(i.get("amount_currency")), bold)
                sheet.write(rowTerminal, col + 6, str(i.get("debit")), bold)
                sheet.write(rowTerminal, col + 7, str(i.get("credit")), bold)
                if i.get("matching_number"):
                    sheet.write(
                        rowTerminal, col + 8, str(i.get("matching_number")), bold
                    )

        rowSon = rowTerminal
        if data.get("Son"):
            for i in data.get("Son"):
                rowSon += 1
                sheet.write(rowSon, col, "Son", bold)
                if i.get("date"):
                    sheet.write(rowSon, col + 1, i.get("date"), bold)
                if i.get("move_id"):
                    sheet.write(rowSon, col + 2, str(i.get("move_id")), bold)
                if i.get("account_id"):
                    sheet.write(rowSon, col + 3, str(i.get("account_id")), bold)
                if i.get("name"):
                    sheet.write(rowSon, col + 4, str(i.get("name")), bold)
                sheet.write(rowSon, col + 5, str(i.get("amount_currency")), bold)
                sheet.write(rowSon, col + 6, str(i.get("debit")), bold)
                sheet.write(rowSon, col + 7, str(i.get("credit")), bold)
                if i.get("matching_number"):
                    sheet.write(rowSon, col + 8, str(i.get("matching_number")), bold)

        rowTransportation = rowSon
        if data.get("Transportation"):
            for i in data.get("Transportation"):
                rowTransportation += 1
                sheet.write(rowTransportation, col, "Transportation", bold)
                if i.get("date"):
                    sheet.write(rowTransportation, col + 1, i.get("date"), bold)
                if i.get("move_id"):
                    sheet.write(rowTransportation, col + 2, str(i.get("move_id")), bold)
                if i.get("account_id"):
                    sheet.write(
                        rowTransportation, col + 3, str(i.get("account_id")), bold
                    )
                if i.get("name"):
                    sheet.write(rowTransportation, col + 4, str(i.get("name")), bold)
                sheet.write(
                    rowTransportation, col + 5, str(i.get("amount_currency")), bold
                )
                sheet.write(rowTransportation, col + 6, str(i.get("debit")), bold)
                sheet.write(rowTransportation, col + 7, str(i.get("credit")), bold)
                if i.get("matching_number"):
                    sheet.write(
                        rowTransportation, col + 8, str(i.get("matching_number")), bold
                    )

        rowShipping = rowTransportation
        if data.get("Shipping"):
            for i in data.get("Shipping"):
                rowShipping += 1
                sheet.write(rowShipping, col, "Shipping", bold)
                if i.get("date"):
                    sheet.write(rowShipping, col + 1, i.get("date"), bold)
                if i.get("move_id"):
                    sheet.write(rowShipping, col + 2, str(i.get("move_id")), bold)
                if i.get("account_id"):
                    sheet.write(rowShipping, col + 3, str(i.get("account_id")), bold)
                if i.get("name"):
                    sheet.write(rowShipping, col + 4, str(i.get("name")), bold)
                sheet.write(rowShipping, col + 5, str(i.get("amount_currency")), bold)
                sheet.write(rowShipping, col + 6, str(i.get("debit")), bold)
                sheet.write(rowShipping, col + 7, str(i.get("credit")), bold)
                if i.get("matching_number"):
                    sheet.write(
                        rowShipping, col + 8, str(i.get("matching_number")), bold
                    )

        rowNFDAC = rowShipping
        if data.get("NFDAC"):
            for i in data.get("NFDAC"):
                rowNFDAC += 1
                sheet.write(rowNFDAC, col, "NFDAC", bold)
                if i.get("date"):
                    sheet.write(rowNFDAC, col + 1, i.get("date"), bold)
                if i.get("move_id"):
                    sheet.write(rowNFDAC, col + 2, str(i.get("move_id")), bold)
                if i.get("account_id"):
                    sheet.write(rowNFDAC, col + 3, str(i.get("account_id")), bold)
                if i.get("name"):
                    sheet.write(rowNFDAC, col + 4, str(i.get("name")), bold)
                sheet.write(rowNFDAC, col + 5, str(i.get("amount_currency")), bold)
                sheet.write(rowNFDAC, col + 6, str(i.get("debit")), bold)
                sheet.write(rowNFDAC, col + 7, str(i.get("credit")), bold)
                if i.get("matching_number"):
                    sheet.write(rowNFDAC, col + 8, str(i.get("matching_number")), bold)

        rowAgency = rowShipping
        if data.get("Agency"):
            for i in data.get("Agency"):
                rowAgency += 1
                sheet.write(rowAgency, col, "Agency", bold)
                if i.get("date"):
                    sheet.write(rowAgency, col + 1, i.get("date"), bold)
                if i.get("move_id"):
                    sheet.write(rowAgency, col + 2, str(i.get("move_id")), bold)
                if i.get("account_id"):
                    sheet.write(rowAgency, col + 3, str(i.get("account_id")), bold)
                if i.get("name"):
                    sheet.write(rowAgency, col + 4, str(i.get("name")), bold)
                sheet.write(rowAgency, col + 5, str(i.get("amount_currency")), bold)
                sheet.write(rowAgency, col + 6, str(i.get("debit")), bold)
                sheet.write(rowAgency, col + 7, str(i.get("credit")), bold)
                if i.get("matching_number"):
                    sheet.write(rowAgency, col + 8, str(i.get("matching_number")), bold)

        rowOthers = rowAgency
        if data.get("Others"):
            for i in data.get("Others"):
                rowOthers += 1
                sheet.write(rowOthers, col, "Others", bold)
                if i.get("date"):
                    sheet.write(rowOthers, col + 1, i.get("date"), bold)
                if i.get("move_id"):
                    sheet.write(rowOthers, col + 2, str(i.get("move_id")), bold)
                if i.get("account_id"):
                    sheet.write(rowOthers, col + 3, str(i.get("account_id")), bold)
                if i.get("name"):
                    sheet.write(rowOthers, col + 4, str(i.get("name")), bold)
                sheet.write(rowOthers, col + 5, str(i.get("amount_currency")), bold)
                sheet.write(rowOthers, col + 6, str(i.get("debit")), bold)
                sheet.write(rowOthers, col + 7, str(i.get("credit")), bold)
                if i.get("matching_number"):
                    sheet.write(rowOthers, col + 8, str(i.get("matching_number")), bold)
