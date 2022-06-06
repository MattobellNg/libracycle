# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'libra circle Customization',
    'summary': '',
    'category': '',
    'description': """
    """,
    'depends': ['project','web','project_project_category'],
    'data': [
        'security/project_access.xml',
        'views/project_views.xml',
    ],
    'qweb': [
    ],
    'auto_install': True,
    'installable': True,
    'assets': {       
        'web.assets_backend': [            
            'customize_vpcs/static/src/js/project_project.js',
        ],
    },
    'license': 'OEEL-1',
}
