# -*- coding: utf-8 -*-
{
    'name': "Customer Routine Report",

    'summary': """
        Customer routine report""",

    'description': """
        Customer routine report
    """,

    'author': "Matt O'Bell Ltd",
    'website': "http://www.mattobell.net",

    'category': 'Uncategorized',
    'version': '0.1',

    'license': 'LGPL-3',

    'depends': ['base', 'report_xlsx'],

    'data': [
        'security/ir.model.access.csv',
        'data/ir_cron.xml',
        'report/tripartite_report/tripartite_report.xml',
        'report/microdaily_report/microdaily_report.xml',
        'report/activity_report/activity_report.xml',
        'report/monthly_invoicing_report/monthly_invoicing_report.xml',
        'data/email_data.xml',
        'views/menus.xml',
        'views/tripartite_report_views.xml',
        'views/microdaily_report_views.xml',
        'views/monthly_invoicing_report_views.xml',
        'views/activity_report_views.xml',
    ],

}
