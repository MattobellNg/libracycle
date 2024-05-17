from collections import OrderedDict
from odoo import models, fields
from odoo.exceptions import UserError


class MicrodailyReport(models.Model):

    _name = 'microdaily.report'
    _description = 'Microdaily Report'

    name = fields.Many2one('res.partner', string='Customer')
    country = fields.Char('Country')
    type_of_kpi = fields.Char('Type of KPI')
    type_of_process = fields.Char('Type of Process')
    stakeholders = fields.Char('Stakeholders')
    code_of_reason = fields.Char('Code of Reason') 	
    month_p = fields.Char('Month - P') 	
    fiscal_week = fields.Char('Fiscal week - Diageo') 	
    clearing_agent = fields.Char('Clearing Agent')  
    clearances_impacted = fields.Char('How many clearances impacted') 	
    po_reference = fields.Char('PO reference')
    supplier_name = fields.Char('Supplier Name')
    type_of_material = fields.Char('Type of material')
    start_date_demurrage = fields.Char('Start date of Demurrage free time (Berth)')
    end_date_demurrage = fields.Char('End date of demurrage free time')
    estimated_value_demurrage = fields.Char('Estimated value of Demurrage in Nairas')
    start_date_port_charges  = fields.Char('Start date of port charges (Berth + 3days)')
    end_date_port_charges = fields.Char('End date of port charges (Gate out)')
    estimate_port_charges = fields.Char('Estimated value of Port charges in Nairas')
    penalty_value = fields.Char('Penalty Value')
    total_costs_paid = fields.Char('Total costs paid')
    root_cause_analyzes = fields.Char('Root Cause Analyzes')
    mitigation_plan = fields.Char('Mitigation Plan took to solve the problem')
    status_of_action = fields.Char('Status of the action')
    custom_release_date = fields.Char('Custom Release Date')
    tdo = fields.Char('TDO')
    delivery_complete_date = fields.Char('DELIVERY COMPLETE DATE (offloaded)')
    	  				

    @classmethod
    def get_report_data(cls, rp):
        if not isinstance(rp, cls):
            raise UserError("Invalid object type")
        report_dict = OrderedDict()
        report_dict.update(
            country=rp.country,
            type_of_kpi=rp.type_of_kpi,
            type_of_process=rp.type_of_process,
            stakeholders=rp.stakeholders,
            code_of_reason=rp.code_of_reason,
            month_p=rp.month_p,
            fiscal_week=rp.fiscal_week,
            clearing_agent=rp.clearing_agent,
            clearances_impacted=rp.clearances_impacted,
            po_reference=rp.po_reference,
            supplier_name=rp.supplier_name,
            type_of_material=rp.type_of_material,
            start_date_demurrage=rp.start_date_demurrage,
            end_date_demurrage=rp.end_date_demurrage,
            estimated_value_demurrage=rp.estimated_value_demurrage,
            start_date_port_charges=rp.start_date_port_charges,
            end_date_port_charges=rp.end_date_port_charges,
            estimate_port_charges=rp.estimate_port_charges,
            penalty_value=rp.penalty_value,
            total_costs_paid=rp.total_costs_paid,
            root_cause_analyzes=rp.root_cause_analyzes,
            mitigation_plan=rp.mitigation_plan,
            status_of_action=rp.status_of_action,
            custom_release_date=rp.custom_release_date,
            tdo=rp.tdo,
            delivery_complete_date=rp.delivery_complete_date,
        )
        return report_dict
