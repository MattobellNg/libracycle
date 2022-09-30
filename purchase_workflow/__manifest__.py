{
    'name': 'Purchase Workflow',
    'version': '15.0.1.0.0',
    'author': 'VperfectCS',
    'website': 'http://www.vperfectcs.com',
    'description': """
    This module coveres following milestones
    (1) Purchase agreement
    """,
    'depends': [
        'ng_internal_requisition',
    ],
    'data': [
        'views/purchase_workflow.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
