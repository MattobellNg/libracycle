# -*- coding: utf-8 -*-
from datetime import date
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import logging
from odoo.addons.base.models.res_partner import WARNING_MESSAGE, WARNING_HELP

_logger = logging.getLogger(__name__)

class Partner(models.Model):

    _inherit = ['res.partner']

    tenant = fields.Boolean('Is a Tenant')

class FacilityBuilding(models.Model):
    _name = 'facility.building'
    _description = 'Building'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Name', required=True)
    apartment_ids = fields.One2many('facility.apartment', 'building_id', string='Apartments')
    active = fields.Boolean(default=True)
    description = fields.Text('Description')

class ApartmentType(models.Model):
    _name = 'apartment.type'
    _description = 'Apartment Type'

    name = fields.Char('Apartment Type')
    active = fields.Boolean(default=True)

class FacilityApartment(models.Model):
    _name = 'facility.apartment'
    _description = 'Apartment'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Name', required=True)
    description = fields.Text('Description')
    current_tenant = fields.Many2one('res.partner', 'Current Tenant',  domain="[('tenant', '=', 1)]")
    apartment_type = fields.Many2one('apartment.type', string='Apartment Type')
    building_id = fields.Many2one('facility.building', string='Building')
    active = fields.Boolean(default=True)
    lock = fields.Selection([
        ('lock', 'Locked'),
        ('unlock', 'UnLocked'),
    ], default='lock', index=True, string="Key", track_visibility='onchange')
    key_log = fields.One2many('key.log', 'apartment_id', track_visibility='onchange')

class KeyLog(models.Model):
    _name = 'key.log'
    _description = 'Key Log'

    name = fields.Char('Title')
    apartment_id = fields.Many2one('facility.apartment', 'Apartment')
    description = fields.Text('Description')
    active = fields.Boolean(default=True)
    responsible_id = fields.Many2one('hr.employee', 'Responsible')
    date = fields.Datetime('Date and Time')
    key_status = fields.Selection([
        ('unlock', 'Key given'),
        ('lock', 'Key returned'),
    ], default='lock', index=True, string="Key Status")
    partner_id = fields.Many2one('res.partner', string='Contractor')
    apartment_lock = fields.Selection([
        ('lock', 'Locked'),
        ('unlock', 'UnLocked'),
    ], default='lock', index=True, string="Key", track_visibility='onchange')

    
    def action_record(self):
        for line in self:
            if line.apartment_lock:
                _logger.info('Log is working')
                line.apartment_id.write({'lock': line.apartment_lock})

class CaseType(models.Model):
    _name = 'case.type'
    _description = 'Case Type'

    name = fields.Char('Case Type')
    active = fields.Boolean(default=True)

class FacilityCase(models.Model):
    _name = 'facility.case'
    _description = 'Case'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Name', required=True, track_visibility='onchange')
    description = fields.Text('Description', track_visibility='onchange')
    tenant_id = fields.Many2one('res.partner', 'Tenant', track_visibility='onchange',  domain="[('tenant', '=', 1)]")
    apartment_id = fields.Many2one('facility.apartment', string='Apartment', track_visibility='onchange')
    type_id = fields.Many2one('case.type', string='Case Type', track_visibility='onchange')
    state = fields.Selection([
        ('draft', 'New'),
        ('in_progress', 'In Progress'),
        ('finished', 'Finished'),
        ('on_hold', 'On Hold'),
        ('cancel', 'Cancelled'),
        ('Closed', 'Closed')
    ], string='Status', group_expand='_expand_states',
       track_visibility='onchange', help='Status of the case', default='draft')
    reason = fields.Text('Reason to close or cancel this case', track_visibility='onchange')
    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Normal'),
        ('2', 'High')
    ], default='0', index=True, string="Priority")
    job_area = fields.Char('Job Area')
    assigned_to = fields.Many2one('hr.employee', 'Assigned To', track_visibility='onchange')
    active = fields.Boolean(default=True)
    date_start = fields.Date('Start Date',default=fields.Date.today)
    date_due = fields.Date('Due Date')
    partner_id = fields.Many2one('res.partner', string='Contractor', domain="[('supplier', '=', 1)]")
    created_by = fields.Many2one('res.partner', 'Created by', track_visibility='onchange')
    date_created = fields.Date(string='Created Date')

    def _expand_states(self, states, domain, order):
        return [key for key, val in type(self).state.selection]

class VisitorLog(models.Model):
    _name = 'visitor.log'
    _description = 'Visitor Log'

    name = fields.Char('Name')
    valid_id = fields.Char('Valid ID')
    time_in = fields.Float('Time IN')
    time_out = fields.Float('Time OUT')
    description = fields.Text('Purpose of work')
    apartment_id = fields.Many2one('facility.apartment', string='Apartment', track_visibility='onchange')
    case_id = fields.Many2one('facility.case', string='Case', track_visibility='onchange')