import time

from odoo import models, fields, api, _
from odoo.exceptions import Warning, ValidationError


class EmployeeAdvanceSalary(models.Model):
    _inherit = "employee.advance.salary"


    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("confirm", "Confirmed"),
            ("approved_dept_manager", "Approved by Department"),
            ("approved_hr_manager", "Approved by HR"),
            ("approved_director", "Approved by Director"),
            ("paid", "Paid"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
            ("reject", "Rejected"),
        ],
        string="State",
        readonly=True,
        default="draft",
        track_visibility="onchange",
    )
    partner_id = fields.Many2one("res.partner", string="Employee Partner")
   



from odoo import models, fields, api, _


class HrJob(models.Model):
    _inherit = "hr.job"

    salary_limit_amount = fields.Float(string="Salary Advance Limit", required=True)