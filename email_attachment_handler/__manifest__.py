{
    'name': 'Email Attachment Handler',
    'version': '0.0.1',
    'category': 'Mail',
    'summary': 'Convert email attachments to downloadable links using Odoo filestore',
    'author': 'MOB - Nneji Ifeanyi',
    'website': 'https://www.mattobell.net',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/attachment_store_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}