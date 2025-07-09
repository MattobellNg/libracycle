{
    'name': 'Document Audit Trail',
    'version': '1.1',
    'category': 'Document Management',
    'summary': 'Track document uploads with user and timestamp information',
    'description': """
        This module extends the document management functionality to track:
        - Who uploaded the document
        - When it was uploaded
        - Last modification details
        - Upload IP address (optional)
        - Shows upload information in chatter
    """,
    'author': 'MOB - Ifeanyi Nneji',
    'website': 'https://www.mattobellonline.com',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_cron.xml',
        'views/ir_attachment_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
    "images": ["static/description/icon.png"] 
}
