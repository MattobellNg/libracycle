from odoo import models, fields, api

class project_project(models.Model):

    _inherit = "project.project"


    mail_temp = fields.Many2one('mail.template',string='Choose a template')
    job_select = fields.Selection([("NAFDAC", "NAFDAC"), ("SON", "SON"),("NESREA","NESREA")],
        "Job selection",
    )
    document = fields.Binary(required=True, attachment=False, help="upload here your document")
    container = fields.Integer(string="Number of Container")