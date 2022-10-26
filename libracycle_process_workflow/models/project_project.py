from urllib.parse import urlencode, urljoin

from odoo import api, fields, models
from odoo.exceptions import ValidationError

class AccountMove(models.Model):
    _inherit = "project.project"


    name = fields.Char(string="Name", store=True)

    _sql_constraints = [
        ('project_uniq_name', 'unique(name)', "Project's name must be unique!"),
    ]