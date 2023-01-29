from odoo import api, fields, models, _
import json


class ProjectReport(models.TransientModel):
    _name = "project.report.wizard"

    duty = fields.Boolean(
        string="Duty",
    )
    terminal = fields.Boolean(
        string="Terminal",
    )
    son = fields.Boolean(
        string="Son",
    )
    shipping = fields.Boolean(
        string="Shipping",
    )
    nfdac = fields.Boolean(
        string="NFDAC",
    )
    agency = fields.Boolean(
        string="Agency",
    )
    other = fields.Boolean(
        string="Others",
    )
    transportation = fields.Boolean(
        string="Transportation",
    )

    def report_download(self):
        selected_rec = self._context.get("active_ids")
        for rec in selected_rec:
            project_rec = self.env["project.project"].search([("id", "=", rec)])
            json_move_line = json.loads(project_rec.move_line.replace("'", '"'))
            duty_rec_id = json_move_line.get("duty")
            shipping_rec_id = json_move_line.get("shipping")
            terminal_rec_id = json_move_line.get("terminal")
            nafdac_rec_id = json_move_line.get("nafdac")
            son_rec_id = json_move_line.get("son")
            agency_rec_id = json_move_line.get("agency")
            transportation_rec_id = json_move_line.get("transportation")
            others_rec_id = json_move_line.get("others")

            duty_rec = self.env["account.move.line"].search_read(
                [("id", "=", duty_rec_id)]
            )
            shipping_rec = self.env["account.move.line"].search_read(
                [("id", "=", shipping_rec_id)]
            )
            terminal_rec = self.env["account.move.line"].search_read(
                [("id", "=", terminal_rec_id)]
            )
            nafdac_rec = self.env["account.move.line"].search_read(
                [("id", "=", nafdac_rec_id)]
            )
            son_rec = self.env["account.move.line"].search_read(
                [("id", "=", son_rec_id)]
            )
            agency_rec = self.env["account.move.line"].search_read(
                [("id", "=", agency_rec_id)]
            )
            transportation_rec = self.env["account.move.line"].search_read(
                [("id", "=", transportation_rec_id)]
            )
            others_rec = self.env["account.move.line"].search_read(
                [("id", "=", others_rec_id)]
            )
            data = {}
            if self.duty:
                data["Duty"] = duty_rec

            if self.terminal:
                data["Terminal"] = terminal_rec

            if self.shipping:
                data["Shipping"] = shipping_rec

            if self.nfdac:
                data["NFDAC"] = nafdac_rec

            if self.son:
                data["Son"] = son_rec

            if self.agency:
                data["Agency"] = agency_rec

            if self.transportation:
                data["Transportation"] = transportation_rec

            if self.other:
                data["Others"] = others_rec

        return self.env.ref(
            "vpcs_project_report_xlsx.report_project_details"
        ).report_action(self, data=data)
