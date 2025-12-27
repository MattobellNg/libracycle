{
    'name': 'Project Approval Workflow',
    'version': '1.0',
    'category': 'Project Management',
    'summary': 'Project approval workflow for post-delivery state',
    'description': """
        This module extends project functionality to handle post-delivery state:
        - Automatically sets status_delivered to True when project reaches post_delivery state
        - Locks the analytic account field when in post_delivery state
    """,
    'author': 'MOB - Ifeanyi Nneji',
    'website': 'https://www.mattobellonline.com',
    'depends': [
        'base',
        'project',
        'customize_vpcs',
    ],
    'data': [
        'views/project_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
    "images": ["static/description/icon.png"] 
}

