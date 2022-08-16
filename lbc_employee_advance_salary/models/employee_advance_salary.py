import time

from odoo import models, fields, api, _
from odoo.exceptions import Warning, ValidationError


class EmployeeAdvanceSalary(models.Model):
    _name = "employee.advance.salary"
    _inherit = "employee.advance.salary"


    state = fields.Selection(
        selection_add=[
            ("admin", "Admin"),
            ("officer", "Officer"),
            ("qac", "QAC"),
            ("director_1", "Director 1"),
            ("director_2", "Director 2"),
             ("confirm",),
        ],
        ondelete={
            "admin": lambda m: m.write({"state": "draft"}),
            "officer": lambda m: m.write({"state": "draft"}),
            "qac": lambda m: m.write({"state": "draft"}),
            "director_1": lambda m: m.write({"state": "draft"}),
            "director_2": lambda m: m.write({"state": "draft"}),
        }
    )
    
    def get_confirm(self):
        self.state = "admin"
        self.confirm_date = fields.Date.today()
        self.confirm_by_id = self.env.user.id
        if self.job_id.salary_limit_amount < self.request_amount:
            raise ValidationError(
                _(
                    "You can not request advance salary more than limit amount, please contact your manager."
                )
            )
   



from odoo import models, fields, api, _


class HrJob(models.Model):
    _inherit = "hr.job"

    salary_limit_amount = fields.Float(string="Salary Advance Limit", required=True)