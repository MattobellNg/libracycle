from odoo import models, fields, api

class ProjectProject(models.Model):
    _inherit = "project.project"

    project_agent_id = fields.Many2one('res.partner', string="Agent Name")
