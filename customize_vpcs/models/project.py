from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import ValidationError

class ProjectProject(models.Model):

    _inherit = "project.project"


    job_select = fields.Selection([("NAFDAC", "NAFDAC"), ("SON", "SON"),("NESREA","NESREA")],
        "Job selection",
    )
    document = fields.Binary(required=True, attachment=False, help="upload here your document")
    container = fields.Integer(string="Number of Container")
    status_delivered = fields.Boolean(string="Delivered")
    status_completed = fields.Boolean(string="Completed")
    start_date = fields.Date(string="Start date")
    end_date = fields.Date(string="End date")
    # this boolean is for edit mode button when button is clicked
    edit_button_check_bool = fields.Boolean(string="check boolean")
    # this boolean is for lock document button when button is clicked
    lock_document_check_bool = fields.Boolean(string="lock document")
    stage_id_done = fields.Boolean(string='Task/Activity Done?')
    date_out = fields.Date(string="Date out",tracking=True,required=True)
    barging_date = fields.Date(string="Barging date",tracking=True,required=True)
    Load_out_date = fields.Date(string="Load out date",tracking=True,required=True)
    offloading_date = fields.Date(string="Offloading date",tracking=True,required=True)
    return_date = fields.Date(string=" Return date",tracking=True,required=True)
    # this boolean field is for if document field is visible or not
    document_show = fields.Boolean(string="document show")


    @api.model
    def visible_button(self):
        get_group = self.env['res.groups'].search([('name','=','lock button')])
        get_department_id = self.env['hr.department'].search([('name','=','QAC')])
        get_employee_id = self.env['hr.employee'].search([('department_id','=',get_department_id.id)]).user_id                      
        get_group.update({
            'users':get_employee_id  
        })

    def lock_document(self):
        for rec in self:
            rec.lock_document_check_bool = True

    def edit_mode(self):
        for rec in self:
            if rec.end_date == fields.Date.today():
                rec.edit_button_check_bool = True

    @api.onchange('project_categ_id')
    def onchange_project_categ_id(self):
        for rec in self:
            if rec.project_categ_id:
                if rec.project_categ_id.document_bool:
                    rec.document_show = True
                else:
                    rec.document_show = False



    @api.onchange('stage_id_done')
    def change_stage_id(self):
        for rec in self:
            if rec.stage_id_done:
                get_stage_id = self.env['project.project.stage'].search([('name','=','Done')])
                if get_stage_id:
                    if not rec.document:
                        raise ValidationError(_("Please upload documents."))
                    else:
                        rec.stage_id = get_stage_id.id

    @api.onchange('stage_id')
    def change_bool_stage(self):
        for rec in self:
            get_stage_id = self.env['project.project.stage'].search([('name','=','Done')])
            if rec.stage_id.id != get_stage_id.id:
                rec.stage_id_done = False

    @api.onchange('status_delivered')
    def action_delivered(self):
        for rec in self:
            if rec.status_delivered == True:
                rec.write({'state':'deliver'})
            else:
                rec.write({'state':'pending'})

    @api.onchange('status_completed')
    def action_completed(self):
        for rec in self:
            if rec.status_completed == True:
                rec.write({'state':'done'})
            else:
                if rec.status_delivered == True:
                    rec.write({'state':'deliver'})
                else:
                    rec.write({'state':'pending'})


    @api.depends("analytic_account_id.credit", "analytic_account_id.debit")
    def _compute_project_balance(self):
        for rec in self:
            rec.analysis_balance = rec.analytic_account_id.balance
            if abs(rec.analytic_account_id.balance) > 0.0 and (rec.state == "pending" or not rec.state):
                rec.state = "progress"
            else:
                if rec.status_delivered == True:
                    if rec.status_completed == True:
                        rec.state = 'done'
                    else:
                        rec.state = 'deliver'               
                else:
                    rec.state = "pending"

   
class ProjectProjectCategory(models.Model):
    _inherit = "project.project.category"

    document_bool = fields.Boolean(string="Document Upload?")