# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Facility Management System',
    'version': '12.0',
    'category': 'Projects',
    'license': 'OPL-1',
    'price': 200.00,
    'images': ['static/description/apartment.PNG'],
    'currency': 'EUR',
    'author': 'oranga',
    'summary': 'Facility Management System',
    'description': """
Facility
Facility Management System
Tenants and Contractors
""",
    'depends': [
        'base',
        'hr',
        'contacts',
        'website',
        'portal',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/facility_view.xml',
        'views/website_register_template.xml',
    ],

    'installable': True,
    'application': True,
}