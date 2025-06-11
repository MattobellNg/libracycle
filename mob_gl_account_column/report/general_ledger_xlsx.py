from odoo import models, _

class GeneralLedgerXslxPatched(models.AbstractModel):
    _inherit = "report.a_f_r.report_general_ledger_xlsx"

    def _get_report_columns(self, report):
        columns = super()._get_report_columns(report)
        next_index = max(columns.keys()) + 1 if columns else 0
        columns[next_index] = {
            "header": _("Account Name"),
            "field": "account_name",
            "width": 30,
        }
        return columns

    def _generate_report_content(self, workbook, report, data, report_data):
        res_data = self.env[
            "report.account_financial_report.general_ledger"
        ]._get_report_values(report, data)
        general_ledger = res_data["general_ledger"]
        accounts_data = res_data["accounts_data"]
        journals_data = res_data["journals_data"]
        taxes_data = res_data["taxes_data"]
        tags_data = res_data["tags_data"]
        filter_partner_ids = res_data["filter_partner_ids"]
        foreign_currency = res_data["foreign_currency"]
        company_currency = report.company_id.currency_id

        for account in general_ledger:
            account_name = accounts_data[account["id"]]["name"]
            self.write_array_title(
                account["code"] + " - " + account_name,
                report_data,
            )

            if "list_grouped" not in account:
                self.write_array_header(report_data)
                account.update(
                    {
                        "initial_debit": account["init_bal"]["debit"],
                        "initial_credit": account["init_bal"]["credit"],
                        "initial_balance": account["init_bal"]["balance"],
                        "account_name": account_name,
                    }
                )
                if foreign_currency:
                    account.update(
                        {"initial_bal_curr": account["init_bal"]["bal_curr"]}
                    )
                self.write_initial_balance_from_dict(account, report_data)

                total_bal_curr = 0
                for line in account["move_lines"]:
                    line.update(
                        {
                            "account": account["code"],
                            "journal": journals_data[line["journal_id"]]["code"],
                            "company_currency_id": company_currency.id,
                            "account_name": account_name,
                        }
                    )
                    if line["currency_id"]:
                        line.update(
                            {
                                "currency_name": line["currency_id"][1],
                                "currency_id": line["currency_id"][0],
                            }
                        )
                    if line["ref_label"] != "Centralized entries":
                        taxes_description = ""
                        tags = ""
                        for tax_id in line["tax_ids"]:
                            taxes_description += taxes_data[tax_id]["tax_name"] + " "
                        if line["tax_line_id"]:
                            taxes_description += line["tax_line_id"][1]
                        for tag_id in line["tag_ids"]:
                            tags += tags_data[tag_id]["name"] + " "
                        line.update(
                            {
                                "taxes_description": taxes_description,
                                "tags": tags,
                            }
                        )
                    if (
                        foreign_currency
                        and line["currency_id"]
                        and line["currency_id"] != company_currency.id
                    ):
                        total_bal_curr += line["bal_curr"]
                        line.update({"total_bal_curr": total_bal_curr})
                    self.write_line_from_dict(line, report_data)
                account.update(
                    {
                        "final_debit": account["fin_bal"]["debit"],
                        "final_credit": account["fin_bal"]["credit"],
                        "final_balance": account["fin_bal"]["balance"],
                        "account_name": account_name,
                    }
                )
                if foreign_currency:
                    account.update(
                        {
                            "final_bal_curr": account["fin_bal"]["bal_curr"],
                        }
                    )
                self.write_ending_balance_from_dict(account, report_data)

            else:
                for group_item in account["list_grouped"]:
                    self.write_array_title(group_item["name"], report_data)
                    self.write_array_header(report_data)
                    group_item.update(
                        {
                            "initial_debit": group_item["init_bal"]["debit"],
                            "initial_credit": group_item["init_bal"]["credit"],
                            "initial_balance": group_item["init_bal"]["balance"],
                            "type": "partner",
                            "grouped_by": account["grouped_by"]
                            if "grouped_by" in account
                            else "",
                            "currency_id": accounts_data[account["id"]]["currency_id"],
                            "account_name": account_name,
                        }
                    )
                    if foreign_currency:
                        group_item.update(
                            {
                                "initial_bal_curr": group_item["init_bal"]["bal_curr"],
                            }
                        )
                    self.write_initial_balance_from_dict(group_item, report_data)

                    total_bal_curr = 0
                    for line in group_item["move_lines"]:
                        line.update(
                            {
                                "account": account["code"],
                                "journal": journals_data[line["journal_id"]]["code"],
                                "company_currency_id": company_currency.id,
                                "account_name": account_name,
                            }
                        )
                        if line["currency_id"]:
                            line.update(
                                {
                                    "currency_name": line["currency_id"][1],
                                    "currency_id": line["currency_id"][0],
                                }
                            )
                        if line["ref_label"] != "Centralized entries":
                            taxes_description = ""
                            tags = ""
                            for tax_id in line["tax_ids"]:
                                taxes_description += (
                                    taxes_data[tax_id]["tax_name"] + " "
                                )
                            for tag_id in line["tag_ids"]:
                                tags += tags_data[tag_id]["name"] + " "
                            line.update(
                                {
                                    "taxes_description": taxes_description,
                                    "tags": tags,
                                }
                            )
                        if (
                            foreign_currency
                            and line["currency_id"]
                            and line["currency_id"] != company_currency.id
                        ):
                            total_bal_curr += line["bal_curr"]
                            line.update({"total_bal_curr": total_bal_curr})
                        self.write_line_from_dict(line, report_data)

                    group_item.update(
                        {
                            "final_debit": group_item["fin_bal"]["debit"],
                            "final_credit": group_item["fin_bal"]["credit"],
                            "final_balance": group_item["fin_bal"]["balance"],
                            "account_name": account_name,
                        }
                    )
                    if foreign_currency and group_item["currency_id"]:
                        group_item.update(
                            {
                                "final_bal_curr": group_item["fin_bal"]["bal_curr"],
                                "currency_name": group_item["currency_id"].name,
                                "currency_id": group_item["currency_id"].id,
                            }
                        )
                    self.write_ending_balance_from_dict(group_item, report_data)
                    report_data["row_pos"] += 1

                if not filter_partner_ids:
                    account.update(
                        {
                            "final_debit": account["fin_bal"]["debit"],
                            "final_credit": account["fin_bal"]["credit"],
                            "final_balance": account["fin_bal"]["balance"],
                            "account_name": account_name,
                        }
                    )
                    if foreign_currency and account["currency_id"]:
                        account.update(
                            {
                                "final_bal_curr": account["fin_bal"]["bal_curr"],
                                "currency_name": account["currency_id"].name,
                                "currency_id": account["currency_id"].id,
                            }
                        )
                    self.write_ending_balance_from_dict(account, report_data)
            report_data["row_pos"] += 2 