# -*- coding: utf-8 -*-
import datetime
from itertools import islice
import json
import xml.etree.ElementTree as ET
import logging
import re
import werkzeug.utils
import werkzeug.wrappers
import base64
import csv
import sys
import io
import tempfile

from odoo import fields
from odoo.http import request, route
from odoo import http, tools, _
from odoo.exceptions import Warning

from odoo.addons.web.controllers.main import WebClient, Binary, Home

SITEMAP_CACHE_TIME = datetime.timedelta(hours=12)

_logger = logging.getLogger(__name__)

class Website(Home):

    @http.route('/facility/check', type='http', auth="user", website=True, cache=300)
    def facility_register(self, **post):
            # freight = request.env['crm.lead'].sudo().search([('name', '=', post['tracking_number'])])
        partner_id = request.env.user.partner_id
        _logger.info("partner ID")
        _logger.info(partner_id)
        apartments = request.env['facility.apartment'].sudo().search([('current_tenant', '=', partner_id.id)])
        _logger.info(apartments)
        values = {
            'apartments': apartments,
        }
        return request.render('facility.apartments_page', values)

    @http.route('/facility/request/create/<int:apartment_id>', type='http', auth="user", website=True, cache=300)
    def facility_apartment(self, apartment_id, **post):
        apartments = request.env['facility.apartment'].browse(apartment_id)
        values = {
            'apartments': apartments,
        }
        return request.render('facility.case_page', values)

    @http.route('/create/request', type='http', auth="public", website=True, cache=300)
    def facility_case_new(self, **post):
        partner_id = request.env.user.partner_id
        apartments = request.env['facility.apartment'].sudo().browse(int(post['apartment_id']))
        _logger.info(apartments)
        values = {
            'name': str(post['name']),
            'description': post['description'],
            'apartment_id': apartments.sudo().id,
            'tenant_id': apartments.sudo().current_tenant.id,
            'created_by': partner_id.sudo().id,
            'date_created': fields.Date.today(),
        }
        request.env['facility.case'].sudo().create(values)
        return request.render('facility.case_success')

    @http.route('/facility/request/view/<int:apartment_id>', type='http', auth="public", website=True, cache=300)
    def facility_view(self, apartment_id, **post):
        cases = request.env['facility.case'].sudo().search([('apartment_id','=', apartment_id)])
        values = {
            'cases': cases,
        }
        return request.render('facility.all_case_page', values)