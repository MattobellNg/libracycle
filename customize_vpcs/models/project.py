from email.policy import default
from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import ValidationError

class ProjectProject(models.Model):

    _inherit = "project.project"


    sn_state = fields.Selection(
        [
            ("pre_alert", "Pre-alert"),
            ("awaiting_arrival", "AWAITING ARRIVAL"),
            ("in_clearing", "IN CLEARING"),
            ("ready_to_load", "READY TO LOAD"),
            ("post_delivery", "POST DELIVERY"),
        ],
        "SN Status",
        default="pre_alert",
        tracking=True,
    )
    sn_status = fields.Selection(
        [
            ("pre_alert", "Pre-alert"),
            ("awaiting_arrival", "AWAITING ARRIVAL"),
            ("in_clearing", "IN CLEARING"),
            ("ready_to_load", "READY TO LOAD"),
            ("post_delivery", "POST DELIVERY"),
        ],
        "SN Status",
        default="pre_alert",
        tracking=True,
    )

################### PRE-ALERT ###################################
    job_refs = fields.Char(string="Job Reference")
    client_name = fields.Many2one('res.partner',string="client name")
    pre_alert_date = fields.Date(string="pre-alert date")
    project_team = fields.Many2one('res.users',string="Project Team")
    account_officer = fields.Many2one('res.users', string="Account Officer")
    item_description = fields.Char(string="Item Description")

    job_form_m_mf = fields.Char(string="Form M(MF)")
    document_job_form_m_mf = fields.Binary(string="Document(Form M(MF))")
    doc_job_bool = fields.Boolean()
    doc_boolean = fields.Boolean()

    mode_shipment = fields.Char(string="Mode Shipment")
################## AWAITING ARRIVAL ############################
    shipping_line = fields.Char(string="Shipping/Air line")
    vessel_line = fields.Char(string="Vessel/Flight name")
    dest_port = fields.Char(string='Destination port')
    terminal = fields.Char(string="Terminal")
    country_of_loading = fields.Many2one('res.country',string="Country of loading")
    port_of_loading = fields.Char(string='PORT OF LOADING')
    rotation_not_received = fields.Date(string="Rotation not received")

    ######base field#####
    document_bol_awb_ref = fields.Binary(string='Document(BOL/AWB)')
    doc_bol_awb_ref = fields.Boolean() 

    document_has_nafdac_1_stamp_date = fields.Binary(string='Document(NAFDAC 1st Stamp)')
    doc_has_nafdac_1_stamp_date = fields.Boolean()

    document_has_nafdac_2_stamp_date = fields.Binary(string='Document(NAFDAC 2nd Stamp)')
    doc_has_nafdac_2_stamp_date = fields.Boolean()

#############################IN CLEARING#################################
    paar_request = fields.Date(string="PAAR REQUEST")

    paar_received = fields.Date(string='PAAR RECEIVED')
    document_paar_received = fields.Binary(string="Document(Paar Received)")
    doc_paar_bool = fields.Boolean()

    duty_assesment = fields.Date(string='Duty Assessment')
    document_duty_assesment = fields.Binary(string='Document(Duty Assessment)')
    doc_duty_asses = fields.Boolean()

    duty_received = fields.Date(string='Duty Received')
    document_duty_received = fields.Binary(string="Document(Document duty received)")
    doc_duty_received = fields.Boolean()

    nafdac_paid = fields.Date(string='Nafdac Paid')
    son_invoice = fields.Date(string='Son Invoice')
    son_paid = fields.Date(string="Son Paid")
    quarantine_payment = fields.Date(string='Quarantine Payment')
    docs_copy_received = fields.Date(string="Complete Copy Docs Received")
    original_copy_received  = fields.Date(string="Complete original Docs Received")
    complete_docs_uploaded = fields.Date(string='Complete Docs uploaded')
    first_shipping_invoice = fields.Date(string="1st Shipping invoice")
    first_shipping_paid = fields.Date(string="1st Shipping paid")
    second_shipping_dn_paid = fields.Date(string="2nd Shipping paid")
    third_shipping_dn_paid = fields.Date(string="3rd Shipping paid")
    first_terminal_invoice = fields.Date(string="1st Terminal invoice")
    first_terminal_paid = fields.Date(string="1st Terminal paid")
    first_additional_storage_paid = fields.Date(string='1st additional storage paid')
    second_additional_storage_paid = fields.Date(string='2nd additional storage paid')
    examination_booked = fields.Date(string="Examination Booked")
    examination_start = fields.Date(string="Examination Start")
    examination_done = fields.Date(string="Examination Done")

    shipping_released = fields.Date(string='Shipping released')
    document_shipping_released = fields.Binary(string='Document(shipping released)')
    doc_ship_released = fields.Boolean()

    fou_approved = fields.Date(string='FOU Approved')
    nepza_released  = fields.Date(string="NEPZA Released")
###########################READY TO LOAD ##############################
    ################needs to be comment#############
    truck_in = fields.Date(string="Truck In")
    gate_out = fields.Date(string="Gate Out")
    empty_container_returned = fields.Date(string="Empty Container Returned")

###############################DELIVERY START(TRUCK/BARGE)####################
    date_delivery_start = fields.Date(string='Date Delivery Start')
    Barge_date = fields.Date(string='Barge Date')
    date_delivery_complete = fields.Date(string='Date Delivery Complete')

    delivery_waybill_from_client = fields.Date(string='Delivery Waybill from Client')
    document_delivery_waybill_from_client = fields.Binary(string='Document(Waybill from Client)')
    doc_waybill_from_client = fields.Boolean()
##################POST DELIVERY###################################

    fecd_rec_date = fields.Date(string='FECD Rec Date')

    fecd_custom_ack = fields.Date(string="FECD Custom ACK")
    document_custom = fields.Binary(string="Document(Custom ACK)")
    doc_custom = fields.Boolean()

    fecd_client_ack = fields.Date(string="FECD Client ACK")
    document_client = fields.Binary(string='Document(Client ACK)')
    doc_client = fields.Boolean()

    nafdac_final_release = fields.Date(string='NAFDAC Final Release')
    document_has_nafdac_final_release = fields.Binary(string='Document(NAFDAC Final Release)')
    doc_nafdac_final_release = fields.Boolean() 

    has_job_refs = fields.Selection(
        [],
        "Job Reference",
        related="project_categ_id.has_job_refs",
        readonly=True,
        default="no",
    )

    has_client_name = fields.Selection(
        [],
        "Client Name",
        related="project_categ_id.has_client_name",
        readonly=True,
        default="no",
    )
    has_pre_alert_date = fields.Selection(
        [],
        "Pre alert date",
        related="project_categ_id.has_pre_alert_date",
        readonly=True,
        default="no",
    )
    has_project_team = fields.Selection(
        [],
        "Project Team",
        related="project_categ_id.has_project_team",
        readonly=True,
        default="no",
    )
    has_account_officer = fields.Selection(
        [],
        "Account Officer",
        related="project_categ_id.has_account_officer",
        readonly=True,
        default="no",
    )
    has_item_description = fields.Selection(
        [],
        "Item Description",
        related="project_categ_id.has_item_description",
        readonly=True,
        default="no",
    )
    has_form_m_mf = fields.Selection(
        [],
        "Form M(MF)",
        related="project_categ_id.has_form_m_mf",
        readonly=True,
        default="no",
    )
    has_mode_shipment = fields.Selection(
        [],
        "Mode Shipment",
        related="project_categ_id.has_mode_shipment",
        readonly=True,
        default="no",
    )
    has_field_visibility = fields.Selection(
        [],
        "Field Visibility",
        related="project_categ_id.has_field_visibility",
        readonly=True
    )
    has_shipping_line = fields.Selection(
        [],
        "SHIPPING LINE/AIR LINE",
        related="project_categ_id.has_shipping_line",
        readonly=True
    )
    has_vessel_name = fields.Selection(
        [],
        "VESSEL /FLIGHT NAME",
        related="project_categ_id.has_vessel_name",
        readonly=True
    )
    has_destination_port = fields.Selection(
        [],
        "DESTINATION PORT (SEA/AIR)",
        related="project_categ_id.has_destination_port",
        readonly=True
    )
    has_terminal = fields.Selection(
        [],
        "TERMINAL",
        related="project_categ_id.has_terminal",
        readonly=True
    )
    has_country_of_loading = fields.Selection(
        [],
        "COUNTRY OF LOADING",
        related="project_categ_id.has_country_of_loading",
        readonly=True
    )
    has_port_of_loading = fields.Selection(
        [],
        "COUNTRY OF LOADING",
        related="project_categ_id.has_port_of_loading",
        readonly=True
    )
    has_rotation_received = fields.Selection(
        [],
        "Rotation not received",
        related="project_categ_id.has_rotation_received",
        readonly=True
    )
    has_paar_request = fields.Selection(
        [],
        "",
        related="project_categ_id.has_paar_request",
        readonly=True
    )
    has_paar_received = fields.Selection(
        [],
        "",
        related="project_categ_id.has_paar_received",
        readonly=True
    )
    has_duty_assesment = fields.Selection(
        [],
        "",
        related="project_categ_id.has_duty_assesment",
        readonly=True
    )
    has_duty_received = fields.Selection(
        [],
        "",
        related="project_categ_id.has_duty_received",
        readonly=True
    )
    has_nafdac_paid = fields.Selection(
        [],
        "",
        related="project_categ_id.has_nafdac_paid",
        readonly=True
    )
    has_son_invoice = fields.Selection(
        [],
        "",
        related="project_categ_id.has_son_invoice",
        readonly=True
    )
    has_son_paid = fields.Selection(
        [],
        "",
        related="project_categ_id.has_son_paid",
        readonly=True
    )
    has_quarantine_payment = fields.Selection(
        [],
        "",
        related="project_categ_id.has_quarantine_payment",
        readonly=True
    )
    has_docs_copy_received = fields.Selection(
        [],
        "",
        related="project_categ_id.has_docs_copy_received",
        readonly=True
    )
    has_original_copy_received = fields.Selection(
        [],
        "",
        related="project_categ_id.has_original_copy_received",
        readonly=True
    )
    has_complete_docs_uploaded = fields.Selection(
        [],
        "",
        related="project_categ_id.has_complete_docs_uploaded",
        readonly=True
    )
    has_1st_shipping_invoice = fields.Selection(
        [],
        "",
        related="project_categ_id.has_1st_shipping_invoice",
        readonly=True
    )
    has_1st_shipping_paid = fields.Selection(
        [],
        "",
        related="project_categ_id.has_1st_shipping_paid",
        readonly=True
    )
    has_2nd_shipping_dn_paid = fields.Selection(
        [],
        "",
        related="project_categ_id.has_2nd_shipping_dn_paid",
        readonly=True
    )
    has_3rd_shipping_dn_paid = fields.Selection(
        [],
        "",
        related="project_categ_id.has_3rd_shipping_dn_paid",
        readonly=True
    )
    has_1st_terminal_invoice = fields.Selection(
        [],
        "",
        related="project_categ_id.has_1st_terminal_invoice",
        readonly=True
    )
    has_1st_terminal_paid = fields.Selection(
        [],
        "",
        related="project_categ_id.has_1st_terminal_paid",
        readonly=True
    )
    has_1st_additional_storage_paid = fields.Selection(
        [],
        "",
        related="project_categ_id.has_1st_additional_storage_paid",
        readonly=True
    )
    has_2nd_additional_storage_paid = fields.Selection(
        [],
        "",
        related="project_categ_id.has_2nd_additional_storage_paid",
        readonly=True
    )
    has_examination_booked = fields.Selection(
        [],
        "",
        related="project_categ_id.has_examination_booked",
        readonly=True
    )
    has_examination_start = fields.Selection(
        [],
        "",
        related="project_categ_id.has_examination_start",
        readonly=True
    )
    has_examination_done = fields.Selection(
        [],
        "",
        related="project_categ_id.has_examination_done",
        readonly=True
    )
    has_shipping_released = fields.Selection(
        [],
        "",
        related="project_categ_id.has_shipping_released",
        readonly=True
    )
    has_fou_approved = fields.Selection(
        [],
        "",
        related="project_categ_id.has_fou_approved",
        readonly=True
    )
    has_nepza_released = fields.Selection(
        [],
        "",
        related="project_categ_id.has_nepza_released",
        readonly=True
    )
        ###############################needs to be comment#####################

    has_truck_in = fields.Selection(
        [],
        "",
        related="project_categ_id.has_truck_in",
        readonly=True
    )
    has_gate_out = fields.Selection(
        [],
        "",
        related="project_categ_id.has_gate_out",
        readonly=True
    )
    has_empty_container_returned = fields.Selection(
        [],
        "",
        related="project_categ_id.has_empty_container_returned",
        readonly=True
    )

    #############################################################
    has_date_delivery_start = fields.Selection(
        [],
        "",
        related="project_categ_id.has_date_delivery_start",
        readonly=True
    )
    has_barge_date = fields.Selection(
        [],
        "",
        related="project_categ_id.has_barge_date",
        readonly=True
    )
    has_date_delivery_complete = fields.Selection(
        [],
        "",
        related="project_categ_id.has_date_delivery_complete",
        readonly=True
    )
    has_delivery_waybill_from_client = fields.Selection(
        [],
        "",
        related="project_categ_id.has_delivery_waybill_from_client",
        readonly=True
    )
    has_fecd_rec_date = fields.Selection(
        [],
        "",
        related="project_categ_id.has_fecd_rec_date",
        readonly=True
    )
    has_fecd_custom_ack = fields.Selection(
        [],
        "",
        related="project_categ_id.has_fecd_custom_ack",
        readonly=True
    )
    has_fecd_client_ack = fields.Selection(
        [],
        "",
        related="project_categ_id.has_fecd_client_ack",
        readonly=True
    )
    has_nafdac_final_release = fields.Selection(
        [],
        "",
        related="project_categ_id.has_nafdac_final_release",
        readonly=True
    )

    job_select = fields.Selection([("NAFDAC", "NAFDAC"), ("SON", "SON"),("NESREA","NESREA")],
        "Job selection",
    )
    job_select_ids = fields.Many2many('job.selection',string='Job selection')
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
    # this boolean is for when status is in completed stage
    state_completed_check_bool = fields.Boolean(string="edit mode close completed")
    #this field is for when QAC clicked the button approval then all the fields of that form is readonly.
    approval_to_readonly_fields_bool = fields.Boolean()

    stage_id_done = fields.Boolean(string='Task/Activity Done?')
    date_out = fields.Date(string="Date out",tracking=True,required=True)
    barging_date = fields.Date(string="Barging date",tracking=True,required=True)
    Load_out_date = fields.Date(string="Load out date",tracking=True,required=True)
    offloading_date = fields.Date(string="Offloading date",tracking=True,required=True)
    return_date = fields.Date(string=" Return date",tracking=True,required=True)
    # this boolean field is for if document field is visible or not
    document_show = fields.Boolean(string="document show")

    def action_truck_loaded(self):       
        composer_form_view_id = self.env.ref('mail.email_compose_message_wizard_form').id

        template_id = self.env.ref('customize_vpcs.email_template').id

        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'view_id': composer_form_view_id,
            'target': 'new',       
            'context': {
                # 'default_composition_mode': 'mass_mail' if len(self.ids) > 1 else 'comment',
                'default_res_id': self.ids[0],
                'default_model': 'project.project',
                'default_use_template': bool(template_id),
                'default_template_id': template_id,
                # 'website_sale_send_recovery_email': True,
                'active_ids': self.ids,
            },     
        }


    def creation_of_purchases_receipt(self):
        self.ensure_one()
        action = self.env.ref("account.action_move_in_receipt_type")
        context = eval(action.context) or {}
        context.update(
            {
                "default_job_id": self.id,
                "default_analytic_account_id": self.analytic_account_id.id,
                "analytic_account_id": self.analytic_account_id.id,
            }
        )

        return {
            "name": action.name,
            "help": action.help,
            "type": action.type,
            # "view_type": action.view_type,
            "view_mode": "form",
            "target": action.target,
            "context": context,
            "res_model": action.res_model,
            "domain": [("job_id", "=", self.id)],
        }

    def new_action_view_purchases_receipt(self):
        # rslt = super(ProjectProject, self).action_view_purchases_receipt()
        self.ensure_one()
        action = self.env.ref("account.action_move_in_receipt_type")

        return {
            "name": action.name,
            "help": action.help,
            "type": action.type,
            # "view_type": action.view_type,
            "view_mode": action.view_mode,
            "target": action.target,
            "context": "{}",
            "res_model": action.res_model,
            "domain": [("job_id", "=", self.id)],
        }


    def pre_alert_button(self):
        pass

    def awaiting_arrival_button(self):
        self.sn_state = 'awaiting_arrival'

    def in_clearing_button(self):
        self.sn_state = 'in_clearing'

    def ready_toload_button(self):
        self.sn_state = 'ready_to_load'

    def post_delivery_button(self):
        self.sn_state = 'post_delivery'

    def back_button(self):
        if self.sn_state == 'awaiting_arrival':
            self.sn_state = 'pre_alert'
        if self.sn_state == 'in_clearing':
            self.sn_state = 'awaiting_arrival'
        if self.sn_state == 'ready_to_load':
            self.sn_state = 'in_clearing'
        if self.sn_state == 'post_delivery':
            self.sn_state = 'ready_to_load'

    @api.onchange('job_form_m_mf','paar_received','duty_assesment','duty_received','shipping_released','fecd_custom_ack','fecd_client_ack','bol_awb_ref','nafdac_1_stamp_date','nafdac_2_stamp_date','delivery_waybill_from_client','nafdac_final_release')
    def onchange_form_doc(self):
        for rec in self:
            if rec.job_form_m_mf:
                rec.doc_job_bool = True
            if rec.paar_received:
                rec.doc_paar_bool = True
            if rec.duty_assesment:
                rec.doc_duty_asses = True
            if rec.duty_received:
                rec.doc_duty_received = True
            if rec.shipping_released:
                rec.doc_ship_released =True
            if rec.fecd_custom_ack:
                rec.doc_custom = True
            if rec.fecd_client_ack:
                rec.doc_client = True
            if rec.bol_awb_ref:
                rec.doc_bol_awb_ref = True
            if rec.nafdac_1_stamp_date:
                rec.doc_has_nafdac_1_stamp_date = True
            if rec.nafdac_2_stamp_date:
                rec.doc_has_nafdac_2_stamp_date = True
            if rec.delivery_waybill_from_client:
                rec.doc_waybill_from_client = True
            if rec.nafdac_final_release:
                rec.doc_nafdac_final_release = True

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

    def approval_to_readonly_fields(self):
        for rec in self:
            if rec.sn_state == 'pre_alert':
                rec.sn_state = 'awaiting_arrival'
            elif rec.sn_state == 'awaiting_arrival':
                rec.sn_state = 'in_clearing'
            elif rec.sn_state == 'in_clearing':
                rec.sn_state = 'ready_to_load'
            elif rec.sn_state == 'ready_to_load':
                rec.sn_state = 'post_delivery'



    # def approval_to_readonly_fields(self):
    #     # for rec in self:
    #     #     rec.approval_to_readonly_fields_bool = True
    #     return self.fields_view_get(view_id=None, view_type=False, toolbar=False,
    #                                                        submenu=False)
    # @api.model
    # def fields_view_get(self, view_id=None, view_type=False, toolbar=False, submenu=False):
    #     print ('___ fields_view_get : ',);
    #     context = self._context
    #     print ('___ context : ', context);
    #     res = super(ProjectProject, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar,
    #                                                        submenu=submenu)
    #     # if context['params']:
    #         # print ('___ context["params"] : ', context['params']);
    #     print ('___ self.approval_to_readonly_fields_bool : ', self.approval_to_readonly_fields_bool);
    #     if self.browse(context.get('active_id')).approval_to_readonly_fields_bool == True:  # Check for context value
    #         print ('___ hello inside method : ', );            
    #         doc = etree.XML(res['arch'])
    #         if view_type == 'form':            # Applies only for form view
    #             for node in doc.xpath("//field"):   # All the view fields to readonly
    #                 node.set('readonly', '1')
    #                 node.set('modifiers', simplejson.dumps({"readonly": True}))

    #             res['arch'] = etree.tostring(doc)
    #     return res

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
                # when status is changed to completed system should make all fields realonly. 
                rec.state_completed_check_bool = True
                # at the same time if edit mode is clicked then it need to be false because of conflict.
                rec.edit_button_check_bool = False                
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

    def toggle_none(self):
        return {
            'Name': 'Schedual items',
            'domain': [('project_id','=',self.id)],
            'res_model': 'project.schedule.items',
            'view_id':False,
            'view_mode':'tree',
            'type':'ir.actions.act_window',
        }


class ProjectScheduleItemsInherit(models.Model):

    _inherit = 'project.schedule.items'

    state = fields.Selection(string='Status', selection=[('in_port', 'In Port'), ('in_transit', 'In Transit'),('barged_out','Barged Out'),('del_ship','Delivered/Shipped'),('return','Return Item')],default='in_port',readonly=True)
    barged_id = fields.Many2one(comodel_name='barged.out', string='Sequence')

    def action_in_transit(self):
        for rec in self:
            rec.state = 'in_transit'

    def action_barged_out(self):
        number = self.env['ir.sequence'].next_by_code('barged.out') or _('New')
        barged = self.env['barged.out'].create({
                'name':number,
            })
        for rec in self:
            rec.state = 'barged_out'
            barged.update({
                'items_ids':[(4,rec.id)]
            })

    def action_dil_ship(self):
        for rec in self:
            rec.state = 'del_ship'

    def action_return_item(self):
        for rec in self:
            rec.state = "return"

class BargedOut(models.Model):
    _name = 'barged.out'

    name = fields.Char('Name')
    items_ids = fields.One2many(comodel_name='project.schedule.items', inverse_name='barged_id', string='Items')
    
class Jobselection(models.Model):

    _name = "job.selection" 

    name = fields.Char(string="Job Selection Name")

class AccountMove(models.Model):

    _inherit = "account.move"

    def action_approve(self):
        for rec in self.invoice_line_ids:
            if rec.price_unit:
                rec.readonly_price_field = True 
        user_id = self.env.user
        print ('___ self.move_type : ', self.move_type);
        if self.move_type == 'in_receipt':
            data = "User : %s approve this receipt on %s"%(user_id.name,datetime.now())
        if self.move_type == 'in_invoice':
            data = "User : %s approve this Vendor bill on %s"%(user_id.name,datetime.now())
        send_message = self.message_post(body=data)

class AccountMoveLine(models.Model):

    _inherit = "account.move.line"

    readonly_price_field = fields.Boolean()