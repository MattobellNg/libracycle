from odoo import models, fields, api, _

FIELD_SELECTION = [("required", "Required"), ("optional", "Optional"), ("no", "None")]


class ProjectProjectCategory(models.Model):
    _inherit = "project.project.category"

    ##########################Pre-alert######################
    has_job_refs = fields.Selection(FIELD_SELECTION, "Job Refs", default="optional",
                                    help="Display job ref on project", )
    has_client_name = fields.Selection(FIELD_SELECTION, "Client Name", default="optional",
                                       help="Display Client Name on project", )
    has_pre_alert_date = fields.Selection(FIELD_SELECTION, "Pre-Alert Date", default="optional",
                                          help="Display Pre-alert date on project", )
    has_project_team = fields.Selection(FIELD_SELECTION, "Project Team", default="optional",
                                        help="Display Project Team on project", )
    has_account_officer = fields.Selection(FIELD_SELECTION, "Account Officer", default="optional",
                                           help="Display Account Officer on project", )
    has_item_description = fields.Selection(FIELD_SELECTION, "Item description", default="optional",
                                            help="Display Item description on project", )
    has_form_m_mf = fields.Selection(FIELD_SELECTION, "Form M (MF)", default="optional",
                                     help="Display Form M (MF) on project")
    has_mode_shipment = fields.Selection(FIELD_SELECTION, "Mode Shipment", default="optional",
                                         help="Display Mode Shipment on project")
    ##########################AWAITING ARRIVAL###########################

    # barge_operator = fields.Many2one('barge.operator',"Barge Operator")
    has_barge_operator = fields.Selection(FIELD_SELECTION, "Barge Operator", default='optional')
    has_duty_assesment = fields.Selection(FIELD_SELECTION, "Duty Assessment", default='optional')
    has_shipping_line = fields.Selection(FIELD_SELECTION, 'Shipping Line/Air Line', default='optional')
    has_vessel_name = fields.Selection(FIELD_SELECTION, 'Vessel/Flight Name', default='optional')
    has_destination_port = fields.Selection(FIELD_SELECTION, 'Destination Port (Sea/Air)', default='optional')
    has_terminal = fields.Selection(FIELD_SELECTION, 'Terminal', default='optional')
    has_country_of_loading = fields.Selection(FIELD_SELECTION, 'County Of Loading', default='optional')
    has_port_of_loading = fields.Selection(FIELD_SELECTION, 'Port Of Loading', default='optional')
    has_rotation_received = fields.Selection(FIELD_SELECTION, 'Rotation Not received', default='optional')
    #############################IN CLEARING#################################
    has_paar_request = fields.Selection(FIELD_SELECTION, "PAAR Request", default="optional")
    has_paar_received = fields.Selection(FIELD_SELECTION, "PAAR Received", default='optional')
    has_agent_name = fields.Selection(FIELD_SELECTION, 'Agent Name', default='no')
    has_duty_received = fields.Selection(FIELD_SELECTION, "Duty Received", default='no')
    has_nafdac_paid = fields.Selection(FIELD_SELECTION, 'NAFDAC Paid', default='no')
    has_son_invoice = fields.Selection(FIELD_SELECTION, "SON Invoice", default='no')
    has_son_paid = fields.Selection(FIELD_SELECTION, "SON Paid", default='no')
    has_quarantine_payment = fields.Selection(FIELD_SELECTION, "Quarantine Payment", default='no')
    has_docs_copy_received = fields.Selection(FIELD_SELECTION, 'Complete Copy Docs Received', default='no')
    has_original_copy_received = fields.Selection(FIELD_SELECTION, 'Complete Original Docs Received', default='no')
    has_complete_docs_uploaded = fields.Selection(FIELD_SELECTION, 'Complete Docs Uploaded', default='no')
    has_1st_shipping_invoice = fields.Selection(FIELD_SELECTION, '1st Shipping Invoice', default='no')
    has_1st_shipping_paid = fields.Selection(FIELD_SELECTION, '1st Shipping Paid', default='no')
    has_2nd_shipping_dn_paid = fields.Selection(FIELD_SELECTION, '2nd Shipping DN Paid', default='no')
    has_3rd_shipping_dn_paid = fields.Selection(FIELD_SELECTION, '3rd Shipping DN Paid', default='no')
    has_1st_terminal_invoice = fields.Selection(FIELD_SELECTION, "1st Terminal Invoice", default='no')
    has_1st_terminal_paid = fields.Selection(FIELD_SELECTION, '1st Terminal Paid', default='no')
    has_1st_additional_storage_paid = fields.Selection(FIELD_SELECTION, '1st Additional Storage Paid', default='no')
    has_2nd_additional_storage_paid = fields.Selection(FIELD_SELECTION, '2nd Additional storage paid', default='no')
    has_examination_booked = fields.Selection(FIELD_SELECTION, 'Examination Booked', default='no')
    has_examination_start = fields.Selection(FIELD_SELECTION, 'Examination start', default='no')
    has_examination_done = fields.Selection(FIELD_SELECTION, 'Examination done', default='no')
    has_shipping_released = fields.Selection(FIELD_SELECTION, 'Shipping Release (DO)', default='no')
    has_fou_approved = fields.Selection(FIELD_SELECTION, 'FOU Approved', default='no')
    has_nepza_released = fields.Selection(FIELD_SELECTION, 'NEPZA Received', default='no')
    ##################READY TO LOAD##################################
    #########################needs to be comment#################

    has_truck_in = fields.Selection(FIELD_SELECTION, 'TRUCK IN ', default='no')
    has_gate_out = fields.Selection(FIELD_SELECTION, 'GATE OUT', default='no')
    has_empty_container_returned = fields.Selection(FIELD_SELECTION, 'EMPTY CONTAINER RETURN', default='no')

    ###############################DELIVERY START(TRUCK/BARGE)####################

    has_date_delivery_start = fields.Selection(FIELD_SELECTION, 'Date Delivery Start', default='no')
    has_barge_date = fields.Selection(FIELD_SELECTION, 'Barge Date', default='no')
    has_date_delivery_complete = fields.Selection(FIELD_SELECTION, 'Date Delivery Complete', default='no')
    has_delivery_waybill_from_client = fields.Selection(FIELD_SELECTION, 'Delivery Waybill from Client', default='no')

    ##################POST DELIVERY###################################

    has_fecd_rec_date = fields.Selection(FIELD_SELECTION, 'FECD Rec Date', default='no')
    has_fecd_custom_ack = fields.Selection(FIELD_SELECTION, 'FECD: customs ACK ', default='no')
    has_fecd_client_ack = fields.Selection(FIELD_SELECTION, 'FECD: To Client ACK', default='no')
    has_nafdac_final_release = fields.Selection(FIELD_SELECTION, 'NAFDAC Final Release', default='no')

    ###############Client Need########################
    has_regulatory_field = fields.Selection(FIELD_SELECTION, 'Regulatory Field', default='optional')
    # has_job_ba_number = fields.Selection(
    #     FIELD_SELECTION,
    #     "BA Number",
    #     # required=True,
    #     default="no",
    #     help="Display BA Number field on project",
    # )

    field_visibility = fields.Selection([
        ('1', 'Delivery only'),
        ('2', 'LPO Financing'),
        ('3', 'Import-Finance Sea'),
        ('4', 'Normal clearing'),
        ('5', 'Fastrack-Sea'),
        ('6', 'TRANSHIRE CLEARING'),
        ('7', 'Free Trade Zone-Sea')
    ], 'Field Visibility', default='1')
    has_field_visibility = fields.Selection([
        ('1', 'Delivery only'),
        ('2', 'LPO Financing'),
        ('3', 'Import-Finance Sea'),
        ('4', 'Normal clearing'),
        ('5', 'Fastrack-Sea'),
        ('6', 'TRANSHIRE CLEARING'),
        ('7', 'Free Trade Zone-Sea')
    ], 'Field Visibility', default='1')
    document_bool = fields.Boolean(string="Document Upload?")
    country_of_destination = fields.Many2one('res.country', string="Destination")

    @api.onchange('has_field_visibility')
    def change_field_combination(self):
        for rec in self:
            if rec.has_field_visibility == '1':
                rec.has_pre_alert_date = "no"
                rec.has_form_m_mf = "no"
                rec.has_mode_shipment = "no"
                rec.has_job_ba_number = "no"
                rec.has_shipping_line = "no"
                rec.has_vessel_name = 'no'
                rec.has_country_of_loading = 'no'
                rec.has_paar_request = 'no'
                rec.has_paar_received = 'no'
                rec.has_duty_assesment = 'no'
                rec.has_duty_received = 'no'
                rec.has_nafdac_paid = 'no'
                rec.has_son_invoice = 'no'
                rec.has_son_paid = 'no'
                rec.has_quarantine_payment = 'no'
                rec.has_docs_copy_received = 'no'
                rec.has_original_copy_received = 'no'
                rec.has_complete_docs_uploaded = 'no'
                rec.has_1st_shipping_invoice = 'no'
                rec.has_1st_shipping_paid = 'no'
                rec.has_2nd_shipping_dn_paid = 'no'
                rec.has_3rd_shipping_dn_paid = 'no'
                rec.has_1st_terminal_invoice = 'no'
                rec.has_1st_terminal_paid = 'no'
                rec.has_1st_additional_storage_paid = 'no'
                rec.has_2nd_additional_storage_paid = 'no'
                rec.has_examination_booked = 'no'
                rec.has_examination_start = 'no'
                rec.has_examination_done = 'no'
                rec.has_shipping_released = 'no'
                rec.has_fou_approved = 'no'
                rec.has_nepza_released = 'no'
                rec.has_fecd_custom_ack = 'no'
                rec.has_fecd_client_ack = 'no'
                rec.has_bol_awb_ref = 'optional'
                rec.has_free_days = 'no'
                rec.has_custom_release_date = 'no'
                rec.has_nafdac_1_stamp_date = 'no'
                rec.has_nafdac_2_stamp_date = 'no'
                rec.has_job_tdo = 'no'
            elif rec.has_field_visibility == '2':
                rec.has_pre_alert_date = "no"
                rec.has_shipping_line = "no"
                rec.has_vessel_name = 'no'
                rec.has_country_of_loading = 'no'
                rec.has_bol_awb_ref = 'optional'
                rec.has_free_days = 'no'
            elif rec.has_field_visibility == '7':
                rec.has_paar_received = 'no'
