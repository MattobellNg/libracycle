import io
import math
import time
from datetime import datetime

from dateutil.relativedelta import relativedelta

from odoo import api, models

try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter


class DynamicReportConfig(models.TransientModel):
    _name = "dynamic.report.config"

    def get_xlsx_report(self, data, response):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {"in_memory": True})
        sheet = workbook.add_worksheet()

        cell_format = workbook.add_format({"font_size": "12px", "bold": True})

        txt = workbook.add_format({"font_size": "10px"})

        x = 0
        y = 0

        if data["filters"]:
            filters = data["filters"]
            if filters.get("date_from"):
                sheet.merge_range(y, x, y, x + 2, filters["date_from"], cell_format)
                x += 2
            if filters.get("date_to"):
                sheet.merge_range(y, x, y, x + 2, filters["date_to"], cell_format)

            x = 0
            if filters.get("date_from") or filters.get("date_to"):
                y += 1

            if filters.get("journal_ids"):
                sheet.merge_range(y, x, y, x + 4, filters["journal_ids"], cell_format)
                y += 1
            x = 0

            for f_val in filters:
                if (
                    f_val in ["date_from", "date_to", "journal_ids"]
                    or not filters[f_val]
                ):
                    continue
                sheet.merge_range(y, x, y, x + 2, filters[f_val], cell_format)
                y += 1

        y += 1
        col_style = cell_format
        col_width = {}
        new_vals = []
        for line in data.get("lines"):
            temp = {}
            for l_col in line:
                temp[int(l_col)] = line[l_col]
            new_vals.append(temp)

        for line in new_vals:
            x = 0
            for col in line:
                col_val = str(line[col]["value"])
                colspan = 0
                if line[col].get("colspan"):
                    colspan = int(line[col]["colspan"])

                col_level = 0
                if line[col].get("level"):
                    col_level = int(line[col]["level"])
                new_col_style = None
                if x == 0 and col_level > 0:
                    new_col_style = workbook.add_format({"font_size": "10px"})

                    if data["report_name"] not in [
                        "journals_audit",
                        "aged_partner",
                        "trial_balance",
                        "partner_ledger",
                        "general_ledger",
                        "tax_report",
                    ]:
                        col_level = math.ceil(col_level / 2)
                    new_col_style.set_indent(col_level)

                if not new_col_style:
                    new_col_style = col_style

                sheet.write(y, x, col_val, new_col_style)

                x += colspan

                if col in col_width:
                    if col_width[col] < colspan:
                        col_width[col] = colspan
                else:
                    col_width[col] = 1

            col_style = txt
            sheet.set_row(y, 25)
            y += 1

        if data["report_name"] in [
            "journals_audit",
            "aged_partner",
            "partner_ledger",
            "general_ledger",
            "tax_report",
        ]:
            min_col_width = 15
        else:
            min_col_width = 30

        for col in col_width:
            width_val = col_width[col] * min_col_width
            if width_val > min_col_width:
                width_val = min_col_width
            sheet.set_column(int(col), int(col), width_val)
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()

    @api.model
    def check_report(self, data):
        print "The DATA", data
        currency_data = {
            "symbol": "",
            "position": "after",
            "decimal_places": 2,
            "company_id": [self.env.user.company_id.id, self.env.user.company_id.name],
        }

        report_lines = []
        if self.env.user.company_id and self.env.user.company_id.currency_id:
            company_id = self.env.user.company_id
            currency_data["symbol"] = company_id.currency_id.symbol
            currency_data["position"] = company_id.currency_id.position
            currency_data["decimal_places"] = company_id.currency_id.decimal_places

        if data["report_type"] == "config":
            ReportObj = self.env["report.account.report_financial"]
            report_lines = ReportObj.get_account_lines(data)
        else:
            if data["project_report_id"][0] == "journals_audit":
                report_lines = {}

                j_ids = []
                for i in data.get("journal_ids"):
                    j_ids.append(int(i))
                data["journal_ids"] = j_ids
                data["used_context"]["journal_ids"] = j_ids

                for journal in j_ids:
                    report_lines[journal] = []
            elif data["project_report_id"][0] == "cap_details":
                ReportObj = self.env["report.project.report_cap_details"]

                partner_ids = []
                report_lines = ReportObj._dynamic_report_lines(data, partner_ids)
            elif data["project_report_id"][0] == "general_ledger":
                ReportObj = self.env["report.account.report_generalledger"]

                report_lines = ReportObj.get_ledger_data(data)
            elif data["project_report_id"][0] == "trial_balance":
                ReportObj = self.env["report.account.report_trialbalance"]

                display_account = data.get("display_account")
                accounts = self.env["account.account"].search([])
                report_lines = ReportObj.with_context(
                    data.get("used_context")
                )._get_accounts_dynamic(accounts, display_account)
            elif data["project_report_id"][0] == "aged_partner":
                res = {}
                ReportObj = self.env["report.account.report_agedpartnerbalance"]

                # build the interval lines
                start = datetime.strptime(data.get("date_from"), "%Y-%m-%d")
                period_length = int(data["period_length"])

                for i in range(5)[::-1]:
                    stop = start - relativedelta(days=period_length - 1)
                    res[str(i)] = {
                        "name": (
                            i != 0
                            and (
                                str((5 - (i + 1)) * period_length)
                                + "-"
                                + str((5 - i) * period_length)
                            )
                            or ("+" + str(4 * period_length))
                        ),
                        "stop": start.strftime("%Y-%m-%d"),
                        "start": (i != 0 and stop.strftime("%Y-%m-%d") or False),
                    }
                    start = stop - relativedelta(days=1)
                data.update(res)
                target_move = data.get("target_move", "all")
                date_from = data.get("date_from", time.strftime("%Y-%m-%d"))

                if data["result_selection"] == "customer":
                    account_type = ["receivable"]
                elif data["result_selection"] == "supplier":
                    account_type = ["payable"]
                else:
                    account_type = ["payable", "receivable"]

                movelines, total, dummy = ReportObj._get_partner_move_lines(
                    account_type, date_from, target_move, int(data["period_length"])
                )

                report_lines = ReportObj.dynamic_report_lines(data, movelines, total)
            elif data["project_report_id"][0] == "tax_report":
                ReportObj = self.env["report.account.report_tax"]

                lines = ReportObj.get_lines(data)

                report_lines = ReportObj.process_lines(lines)

        return [report_lines, currency_data]


class ReportProjectDetails(models.AbstractModel):
    _name = "report.project.report_cap_details"

    def _dynamic_report_lines(self, data, project):
        query = """
        SELECT "project_project".id,"account_analytic_account".name AS job_name,"project_project".bol_awb_ref AS bol_awb,"project_project".client_ref AS ref,"project_project".items_total_size AS container_size,
        "project_project".schedule_item_count AS count,"project_project".items_total_weight AS weight,"project_project".job_cbm AS general_cargo,"project_project_category".name AS job_dynamics, "project_project".state AS job_status,
        "account_invoice".number AS invoice_no,"account_invoice".name AS invoice_name,"account_invoice".amount_untaxed AS amount_untaxed,"account_invoice".amount_tax AS amount_tax,"account_invoice".create_date AS prepared_date,
        "account_invoice".create_date AS submitted_date,"account_invoice".date_due AS due_date,"account_payment".amount AS amount_paid,("account_invoice".amount_untaxed - "account_invoice".amount_tax) AS total_invoice,
        "account_payment".payment_date AS payment_date,"res_partner".name AS client_name,"res_currency".name AS currency_name,"res_currency".symbol AS currency_symbol, ("account_payment".amount  - "account_invoice".amount_untaxed) AS tot_balance
        FROM account_invoice 
        LEFT JOIN account_invoice_line ON ("account_invoice_line".invoice_id = "account_invoice".id) 
        LEFT JOIN account_invoice_payment_rel ON ("account_invoice_payment_rel".invoice_id = "account_invoice".id) 
        LEFT JOIN account_payment ON ("account_invoice_payment_rel".payment_id = "account_payment".id) 
        LEFT JOIN account_analytic_account ON ("account_invoice_line".account_analytic_id = "account_analytic_account".id) 
        LEFT JOIN project_project ON ("project_project".analytic_account_id = "account_analytic_account".id) 
        LEFT JOIN project_project_category ON ("project_project".project_categ_id = "project_project_category".id) 
        INNER JOIN res_partner ON ("account_invoice".commercial_partner_id = "res_partner".id) AND ("account_invoice".partner_id = "res_partner".id) 
        INNER JOIN res_currency ON ("account_invoice".currency_id = "res_currency".id) AND ("account_invoice_line".currency_id = "res_currency".id) AND ("account_payment".currency_id = "res_currency".id) 
        WHERE "account_invoice".type = 'out_invoice' AND "project_project".active = True"""
        self.env.cr.execute(query)
        res = self.env.cr.dictfetchall()
        return res


class ReportDynamicPDF(models.AbstractModel):
    _name = "report.phlema_project_reports.phl_project_reports_pdf"

    def get_report_values(self, docids, data=None):
        return data
