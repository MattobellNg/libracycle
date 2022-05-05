# Copyright 2015-2017 Tecnativa - Jairo Llopis <jairo.llopis@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError


class PartnerExtensionRec(models.Model):
    _inherit = "res.partner"

    is_carrier_partner = fields.Boolean("Carrier Company", default=False)


class ProjectPort(models.Model):
    _name = "project.port"

    name = fields.Char("Port Name", required=True)
    address = fields.Text("Port Address")
    port_country_id = fields.Many2one("res.country", "Port country", required=True)
    port_state_id = fields.Many2one(
        "res.country.state",
        "Port state",
        required=True,
        domain="[('country_id', '=', port_country_id)]",
    )


class ProjectTerminal(models.Model):
    _name = "project.terminal"

    name = fields.Char("Terminal Name", required=True)
    address = fields.Text("Terminal Address")
    terminal_country_id = fields.Many2one("res.country", "Terminal country", required=True)
    terminal_state_id = fields.Many2one(
        "res.country.state",
        "Terminal state",
        required=True,
        domain="[('country_id', '=', terminal_country_id)]",
    )


class ProjectScheduleItems(models.Model):
    _name = "project.schedule.items"
    _description = "Project schedule items"

    sequence = fields.Integer("Sequence")
    name = fields.Char("Item Code", required=True)
    project_id = fields.Many2one("project.project", "related project")
    project_type_id = fields.Many2one("project.type", "Project Type", related="project_id.type_id", store=True)
    project_service_means = fields.Selection(related="project_type_id.service_means_type", store=True)
    product_id = fields.Many2one(
        "product.product",
        "Item Type",
        required=True,
        domain="[('is_project_item', '=', True), ('project_type_id', '=', project_type_id)]",
    )
    project_order_id = fields.Many2one("sale.order", "Related sales order")
    description = fields.Char("Item Description", compute="_compute_item_val")
    size = fields.Float(string="Size", required=True)
    product_uom_id = fields.Many2one("uom.uom", "Unit of Measure")
    product_mesured_as = fields.Selection(related="product_uom_id.unit_measured_as", store=True)
    unit = fields.Selection([("ft", "Feet"), ("kg", "Kilogram")], "Unit", default="ft")

    @api.model
    def create(self, vals):
        result = super(ProjectScheduleItems, self).create(vals)
        if result:
            # Get project record
            proj = self.env["project.project"].browse(int(result.project_id.id))
            if proj:
                item_weight = proj.items_total_weight or 0.00
                item_size = proj.items_total_size or 0.00
                item_cnt = proj.schedule_item_count + 1
                product_mesured_as = result.product_mesured_as
                if product_mesured_as == "wgt":
                    item_weight = item_weight + result.size
                else:
                    item_size = item_size + result.size
                proj.write(
                    {
                        "items_total_size": item_size,
                        "items_total_weight": item_weight,
                        "schedule_item_count": item_cnt,
                    }
                )
        return result

    def write(self, vals):
        result = super(ProjectScheduleItems, self).write(vals)
        if result:
            for rec in self:
                proj_schedule = rec.project_id.project_schedule_items_ids
                if proj_schedule:
                    item_cnt = len(proj_schedule)
                    item_weight = 0.00
                    item_size = 0.00
                    for rec in proj_schedule:
                        if rec.product_mesured_as == "wgt":
                            item_weight = item_weight + rec.size
                        else:
                            item_size = item_size + rec.size

                    #
                    rec.project_id.write(
                        {
                            "items_total_size": item_size,
                            "items_total_weight": item_weight,
                            "schedule_item_count": item_cnt,
                        }
                    )
        return result

    @api.depends("size", "product_uom_id")
    def _compute_item_val(self):
        for rec in self:
            if rec.size and rec.product_uom_id:
                rec.description = "%s%s" % (rec.size, rec.product_uom_id.name)

    @api.onchange("product_id", "product_uom_id")
    def onchange_product_id(self):
        if self.product_id:
            # self.lots_visible = self.product_id.tracking != 'none'
            if not self.product_uom_id or self.product_uom_id.category_id != self.product_id.uom_id.category_id:
                self.product_uom_id = self.product_id.uom_id.id
            res = {"domain": {"product_uom_id": [("category_id", "=", self.product_uom_id.category_id.id)]}}
        else:
            res = {"domain": {"product_uom_id": []}}
        return res


class ProjectProject(models.Model):
    # _inherit = ""
    _name = "project.project"
    _inherit = ["project.project", "mail.thread"]

    description = fields.Html()
    job_allocation_date = fields.Date(
        "Allocation Date",
        required=True,
        track_visibility="onchange",
    )
    client_ref = fields.Char(
        "Client Ref.",
        oldname="x_clientref",
        track_visibility="onchange",
    )
    job_form_m = fields.Char(
        "Form M./NXP",
        oldname="x_formm",
        track_visibility="onchange",
    )
    job_form_m_date = fields.Date(
        "Form M./NXP Collection",
        track_visibility="onchange",
    )
    bol_awb_ref = fields.Char(
        "BOL/AWB Number",
        oldname="x_bol_awb",
        track_visibility="onchange",
    )
    job_carrier_id = fields.Many2one(
        "res.partner",
        string="Carrier",
        oldname="x_carrier",
        help="Ensure partner carrier flag is enable on partner",
        track_visibility="onchange",
    )
    discharge_port_id = fields.Many2one(
        "project.port",
        "Discharge Port",
        required=True,
        track_visibility="onchange",
    )
    loading_port_id = fields.Many2one(
        "project.port",
        "Loading Port",
        required=True,
        track_visibility="onchange",
    )

    loading_terminal_id = fields.Many2one(
        "stock.location",
        "Loading Terminal",
        required=True,
        track_visibility="onchange",
    )
    discharge_terminal_id = fields.Many2one(
        "stock.location",
        "Discharge Terminal",
        required=True,
        track_visibility="onchange",
        domain=[("usage", "in", ["transit", "internal"])],
    )
    clearing_agent_id = fields.Many2one("res.partner", string="Clearing Agents", domain=[("supplier", "=", True)])
    vessel_det = fields.Char("Vessel", oldname="x_vessel", track_visibility="onchange")
    origin_country_id = fields.Many2one(
        "res.country",
        "Country of origin",
        required=True,
        track_visibility="onchange",
    )
    destination_country_id = fields.Many2one(
        "res.country",
        "Country of destination",
        required=True,
        track_visibility="onchange",
    )
    items_count = fields.Integer(compute="_compute_items_count", string="Tasks")
    project_schedule_items_ids = fields.One2many("project.schedule.items", "project_id", "Job Items")
    schedule_item_count = fields.Integer("Counts")
    items_total_weight = fields.Float("Weight", default=0.0)
    items_total_size = fields.Float("Size", default=0.0)
    analysis_balance = fields.Monetary(compute="_compute_project_balance", string="Balance")
    arrival_date = fields.Date(
        "Arrival Date",
        track_visibility="onchange",
    )
    job_son = fields.Char(
        "SON",
        track_visibility="onchange",
    )
    job_liner = fields.Char(
        "TERMINAL",
        track_visibility="onchange",
    )
    job_ba_number = fields.Char(
        "BA Number",
        track_visibility="onchange",
    )
    job_cbm = fields.Char(
        "CBM",
        track_visibility="onchange",
    )
    bill_of_lading = fields.Date(
        "Bill of lading",
        track_visibility="onchange",
    )
    shipping_doc = fields.Date(
        "Shipping Doc",
        track_visibility="onchange",
    )
    job_paar = fields.Date(
        "PAAR/NEPZA",
        track_visibility="onchange",
    )
    job_assessment = fields.Date(
        "Assessment Notice",
        track_visibility="onchange",
    )
    job_duty = fields.Date(
        "Duty Payment Date",
        track_visibility="onchange",
    )
    job_shipping_co = fields.Selection(
        [("unpaid", "UNPAID"), ("paid", "PAID")],
        "Shipping Co/Airline",
        default="unpaid",
        track_visibility="onchange",
    )
    job_terminal_payment = fields.Selection(
        [("unpaid", "UNPAID"), ("paid", "PAID")],
        "Terminal Payment",
        default="unpaid",
        track_visibility="onchange",
    )
    custom_release_date = fields.Date("Custom Release Date", track_visibility="onchange")
    job_tdo = fields.Date("TDO", track_visibility="onchange")
    job_plant_delivery_date = fields.Date(
        "Plan delivery date",
        track_visibility="onchange",
    )
    exchange_control_returned = fields.Date(
        "Exchange control returned",
        track_visibility="onchange",
    )

    shipping_rating_till = fields.Date(
        "Shipping Rate Till",
        track_visibility="onchange",
    )
    terminal_rating_till = fields.Date(
        "Terminal Rate Till",
        track_visibility="onchange",
    )
    cleared_date = fields.Date(
        "Cleared Date",
        track_visibility="onchange",
    )
    loading_date = fields.Date(
        "Loading Date",
        track_visibility="onchange",
    )
    delivery_date = fields.Date(
        "Delivery Date",
        track_visibility="onchange",
    )
    container_return_date = fields.Date(
        "Container Return Date",
        track_visibility="onchange",
    )
    total_cycle = fields.Char(
        "Total Cycle",
        compute="_cal_total_cycle",
        store=True,
        default="0",
        track_visibility="onchange",
    )
    job_do = fields.Date(
        "DO",
        track_visibility="onchange",
    )
    ecd_date = fields.Date(
        "ECD Date",
        track_visibility="onchange",
    )
    refund_demurrage_option = fields.Selection(
        [("none", "None"), ("refund", "Refund"), ("demurrage", "Demurrage")],
        "Demurrage/Refund",
        default="none",
        track_visibility="onchange",
    )
    refund_demurrage_benef_id = fields.Many2one("res.partner", "R/D Beneficiary", track_visibility="onchange")
    refund_demurrage_amount = fields.Float("Amount", track_visibility="onchange")

    cdr_beneficiary_id = fields.Many2one("res.partner", "CDR Beneficiary", track_visibility="onchange")
    cdr_amount_deposit = fields.Float(
        "Amount Deposited",
        track_visibility="onchange",
    )
    cdr_amount_paid = fields.Float(
        "Amount Paid",
        track_visibility="onchange",
    )
    cdr_comment = fields.Char(
        "cdr comment",
        track_visibility="onchange",
    )

    etr_invoice_number = fields.Char(
        "Invoice Number",
        track_visibility="onchange",
    )
    etr_credit_memo = fields.Float(
        "Credit Memo",
        track_visibility="onchange",
    )
    etr_amount = fields.Float(
        "Amount",
        track_visibility="onchange",
    )

    etd = fields.Date("ETD", track_visibility="onchange")
    eta = fields.Date("ETA", track_visibility="onchange")
    ata = fields.Date("ATA", track_visibility="onchange")
    discharge_date = fields.Date("Discharge Date", track_visibility="onchange")
    doc_to_agent = fields.Char("Doc. to agent", track_visibility="onchange")
    rotation_number = fields.Char("Rotation Number", track_visibility="onchange")
    nafdac_1_stamp_date = fields.Date("NAFDAC 1st stamp date", track_visibility="onchange")
    nafdac_2_stamp_date = fields.Date("NAFDAC 2nd stamp sate", track_visibility="onchange")
    son_date = fields.Date("SON date", track_visibility="onchange")
    pod = fields.Char("POD", track_visibility="onchange")
    free_days = fields.Char("No of Free days", track_visibility="onchange")
    custom_exam_date = fields.Date("Custom Exams Booking Date", track_visibility="onchange")
    custom_date = fields.Date("Custom Exams Date", track_visibility="onchange")
    fou_release_date = fields.Date("FOU release Date", track_visibility="onchange")
    gate_release_date = fields.Date("Gate release Date", track_visibility="onchange")
    empty_container_return_date = fields.Date("Empty Container return Date", track_visibility="onchange")
    job_invoiced = fields.Selection(
        [("yes", "YES"), ("no", "NO")],
        "Job Invoiced",
        default="no",
        compute="_check_invoiced_job",
        store=True,
    )

    last_project_comment = fields.Char("Project Comment", compute="_project_message_comment")

    state = fields.Selection(
        [
            ("new", "New"),
            ("pending", "Pending"),
            ("progress", "In progress"),
            ("deliver", "Delivered"),
            ("cancel", "Cancelled"),
            ("done", "Completed"),
        ],
        "Status",
        default="new",
        track_visibility="onchange",
    )

    invoice_nos = fields.Char("Invoice No(s)")
    invoice_amount = fields.Char("Invoice Amount")
    invoice_date = fields.Char("Invoice Date")
    invoice_payment_date = fields.Char("Invoice Payment Date")

    def create(self, vals):
        if vals.get("state"):
            if vals.get("state") == "new":
                vals["state"] = "pending"
        if vals.get("user_id"):
            employee_id = self.env["hr.employee"].sudo().search([("user_id", "=", int(vals.get("user_id")))])
            if not employee_id:
                raise UserError("Project manager has no related user assigned on hr settings")
        return super(ProjectProject, self).create(vals)

    @api.depends("delivery_date", "analytic_account_id.credit")
    def _check_invoiced_job(self):
        for rec in self:
            proj_sales_order = rec.project_sales_order_ids
            if proj_sales_order:
                if any(order.invoice_status in ["invoiced"] for order in proj_sales_order) and rec.delivery_date:
                    rec.job_invoiced = "yes"
                else:
                    rec.job_invoiced = "no"

    @api.depends("message_ids")
    def _project_message_comment(self):
        for rec in self:
            if rec.message_ids:
                check_for_comment = rec.env["mail.message"].search(
                    [
                        ("model", "=", "project.project"),
                        ("res_id", "=", rec.id),
                        ("message_type", "=", "comment"),
                    ],
                    order="date desc",
                    limit=1,
                )
                if check_for_comment:
                    rec.last_project_comment = check_for_comment.body

    @api.depends("cleared_date", "job_duty")
    def _cal_total_cycle(self):
        for rec in self:
            if rec.cleared_date and rec.job_duty:
                cal_days = rec.cleared_date - rec.job_duty
                if cal_days:
                    rec.total_cycle = "%s day(s)" % cal_days

    @api.onchange("user_id")
    def on_change_task_assign_id(self):
        if self.user_id:
            employee_rec = self.user_id._get_related_employees()
            if not employee_rec:
                raise UserError("%s has no related user on hr settings" % self.user_id.name)

    @api.depends("analytic_account_id.credit", "analytic_account_id.debit")
    def _compute_project_balance(self):
        for rec in self:
            rec.analysis_balance = rec.analytic_account_id.balance
            if abs(rec.analytic_account_id.balance) > 0.0 and (rec.state == "pending" or not rec.state):
                rec.state = "progress"
            else:
                rec.state = "pending"

    def action_view_cost_revenue(self):
        self.ensure_one()
        action = self.env.ref("analytic.action_analytic_account_form")

        return {
            "name": action.name,
            "help": action.help,
            "type": action.type,
            "view_type": action.view_type,
            "view_mode": action.view_mode,
            "target": action.target,
            "context": "{}",
            "res_model": action.res_model,
            "domain": [("id", "=", self.analytic_account_id.id)],
        }

    def import_schedule_item(self):
        """return action to import bank/cash statements. This button should be called only on journals with type =='bank'"""
        action_name = "action_project_schedule_item_import"
        [action] = self.env.ref("project_description.%s" % action_name).read()
        # Note: this drops action['context'], which is a dict stored as a string, which is not easy to update
        action.update({"context": ("{'project_id': " + str(self.id) + "}")})
        return action

    def download_schedule_item_csv(self):
        """return action to import bank/cash statements. This button should be called only on journals with type =='bank'"""
        action_name = "action_project_schedule_item_download"
        [action] = self.env.ref("project_description.%s" % action_name).read()
        # Note: this drops action['context'], which is a dict stored as a string, which is not easy to update
        action.update({"context": ("{'default_project_type_id': " + str(self.type_id.id) + "}")})
        return action

    def _compute_items_count(self):
        for project in self:
            project.items_count = len(project.project_schedule_items_ids)

    def toggle_none(self):
        return False

    def action_pending(self):
        self.write({"state": "pending"})

    def action_progress(self):
        self.write({"state": "progress"})

    def action_done(self):
        self.write({"state": "done"})

    def action_draft(self):
        self.write({"state": "draft"})


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"
    _description = "Analytic Line"

    project_rec_id = fields.Many2one("project.project", "Project")

    @api.model
    def create(self, vals):
        res = super(AccountAnalyticLine, self).create(vals)
        if res:
            if vals.get("account_id"):
                # Get project record and change it state
                proj_acc_id = int(vals.get("account_id"))
                proj_rec = self.env["project.project"].search(
                    [
                        ("state", "=", "pending"),
                        ("analytic_account_id", "=", proj_acc_id),
                    ]
                )
                if proj_rec:
                    proj_rec.action_progress()
        return res
