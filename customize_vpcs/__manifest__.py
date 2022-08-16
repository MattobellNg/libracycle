# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'libra circle Customization',
    'version': '15.0.1.0.0',
    'author': 'VperfectCS',
    'website': 'http://www.vperfectcs.com',
    'description': """
    This module coveres following milestones
    (1) Project
    (2) QAC
    """,
    'depends': ['project','web','project_project_category','report_xlsx'],
    'data': [
        'security/project_access.xml',
        "security/ir.model.access.csv",
        "data/seq.xml",
        "data/batch_action.xml",
        "data/batch_action_tracking.xml",
        'views/project_views.xml',
        'views/project_project_category.xml',
        "data/email_template.xml",
        "report/report.xml",
        "report/report_pdf.xml",
        "report/waybill_report.xml",
    ],
    'qweb': [
    ],
    'auto_install': True,
    'installable': True,
    'assets': {       
        'web.assets_backend': [            
            # 'customize_vpcs/static/src/js/project_project.js',
        ],
    },
    'license': 'OEEL-1',
}