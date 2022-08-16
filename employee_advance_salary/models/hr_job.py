#!/usr/bin/python
# -*- coding: utf-8 -*-

# from openerp import models, fields, api, _
from odoo import models, fields, api, _


class HrJob(models.Model):
    _inherit = 'hr.job'
    
    salary_limit_amount = fields.Float(string='Salary Limit', required=True)
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
