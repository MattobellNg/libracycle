# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Project(models.Model):
    _name = 'project.project'
    _inherit = 'project.project'

    mode_shipment_air_sea = fields.Many2one('mode.shipment', string="Mode Shipment(Air/Sea)")


