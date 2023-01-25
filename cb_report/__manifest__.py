# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'C&B Report',
    'version': '15.0.1.0.0',
    'author': 'VperfectCS',
    'website': 'http://www.vperfectcs.com',
    'description': """
    """,
    'depends': ['customize_vpcs','report_xlsx'],
    'data': [        
        'security/CBreport.xml',
        "security/ir.model.access.csv",
        "data/cb_report_action.xml",
        "views/cb_report.xml",
        "views/product_template.xml",
        "views/project_views.xml",
        "wizard/view_wiz_report.xml",        
    ],
    'qweb': [
    ],
    'auto_install': True,
    'installable': True,
    'license': 'OEEL-1',
}