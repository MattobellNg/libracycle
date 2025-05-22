{
    'name': 'Custom C&B Report Sales View',
    'version': '15.0.0.0.4',
    'summary': 'Customizes the Jobs list view for Sales (C&B Report) with different columns and labels.',
    'description': """
    Customizes the Jobs list view for Sales (C&B Report) with different columns and labels.
    """,
    'author': 'MOB - Nneji Ifeanyi',
    'website': 'https://www.mattobellonline.com',
    'category': 'Project',
    'depends': ['project', 'customize_vpcs', 'cb_report'],
    'data': [
        'views/project_project_sales_tree.xml',
        'views/menu_action_override.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
