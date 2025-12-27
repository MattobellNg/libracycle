{
    'name': 'Project Agent Name',
    'version': '1.0',
    'category': 'Project',
    'summary': 'Add agent name as res.partner field',
    'description': """
        This module adds a new agent name field that links to res.partner
        and replaces the original char field from customize_vpcs.
    """,
    'author': 'MOB - Nneji Ifeanyi',
    'website': 'https://www.mattobellonline.com',
    'depends': ['customize_vpcs'],
    'data': [
        'views/project_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
    "images": ["static/description/icon.png"] 
}
