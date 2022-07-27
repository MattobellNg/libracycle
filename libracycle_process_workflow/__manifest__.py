{
    "name": "Libra Payment Process Flow",
    "summary": """Libra Payment Process Flow""",
    "description": """
        Libra Payment Process Flow
    """,
    "author": "Matt O'Bell",
    "website": "http://www.yourcompany.com",
    "version": "1.2.2",
    "depends": ["base", "account_accountant", "purchase_requisition"],
    "data": [
        # 'security/ir.model.access.csv',
        "security/res_group.xml",
        "views/account_move.xml",
        "views/templates.xml",
        "data/mail_template.xml",
    ],
    "license": "LGPL-3",
}
