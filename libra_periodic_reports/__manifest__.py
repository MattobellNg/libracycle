# -*- coding: utf-8 -*-
{
    'name': "Libracircle Periodic Report",

    'summary': """
        Libracircle periodic report""",

    'description': """
        Libracircle periodic report
    """,

    'author': "Matt O'Bell Ltd",
    'website': "http://www.mattobell.net",

    'category': 'Uncategorized',
    'version': '0.1',

    'license': 'LGPL-3',

    'depends': ['mail'],

    'data': [
        'security/ir.model.access.csv',
        'data/ir_cron.xml',
        'data/email_data.xml',
        'views/menus.xml',
        'views/activity_report_views.xml',
        'views/microdaily_report_views.xml',
        'views/monthly_invoicing_report_views.xml',
        'views/tripartite_report_views.xml',
    ],

}
