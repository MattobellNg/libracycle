# -*- coding: utf-8 -*-
{
	'name': 'ReportMate',

	'summary': """
Complex data in a single view,dynamic reports,sale report,create reports,
                custom reports,Create Custom View,report Security,custom query,
                pivot view report,tree view report,list view report,graph view report,
                display complex data,create custom report
""",

	'description': """
Best Custom Report Apps,
        Custom Report Apps,
        Custom Reports,
        Report Mate,
        Custom View Apps,
        Report Maker,
        Custom Field,
        Tree View Report,
        Tree View Model,
        Tree View Table,
        Odoo View,
        Odoo Report,
        Table View,
        Sales Custom Report,
        Product Custom Report,
        Odoo Custom Report Apps,
        accounting report,
        List View Report,
        List View Table,
        Pivot View Report,
        Pivot View Model,
        Pivot View Table,
        Graph View Model,
        Graph View Report,
        Graph View Table,
        Custom Report Creator Apps,
        GTS Custom report,
        Financial Report,
        Move Report,
        Flat Data Structure View,
        Widget View,
        Sale order custom report,
        Report View Apps,
        Report Creator Apps,
        Custom Report Creator Apps,
        ReportMate Report,
        Reports, reports apps, 
        rports, 
        reports, 
        Pivot view report, 
        graph view report,
        reports by email, 
        custom reports, 
        pos reports, 
        collection reports, 
        accounting, 
        dynamic financial reports, 
        financial reports, financial reports v14, 
        multi branch applications, 
        overdue payment reports, 
        report, 
        reporting application
    """,
    'author': "Ksolves India Ltd.",
    'license': 'OPL-1',
    'currency': 'EUR',
    'price': 175.2,
    'website': "https://store.ksolves.com/",
    'maintainer': 'Ksolves India Ltd.',
    'category': 'Tools',
    'version': '15.0.1.0.0',
    'support': 'sales@ksolves.com',
    'images': ['static/description/report_mate_1.gif'],
    'live_test_url': 'http://reportmate15.kappso.in/web/login',
    'depends': ['base', 'web'],
    'data': [
        'security/ks_security_groups.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/views.xml',
    ],
    'assets': {
      'web.assets_backend': [
          'ks_custom_report/static/src/css/ks_custom_report.css',
          'ks_custom_report/static/src/js/ks_model_relation_widget.js',
          'ks_custom_report/static/src/js/ks_graph_renderer.js',
          'ks_custom_report/static/src/js/ks_graphModel.js',
      ],
    },

    'demo': [
        'demo/demo.xml',
    ],

    'installable': True,
    'application': True,

    'uninstall_hook': 'uninstall_hook',

}
