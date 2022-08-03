{
    "name": "Libra Payment Process Flow",
    "summary": """Libra Payment Process Flow""",
    "description": """
        Libra Payment Process Flow
    """,
    "author": "Matt O'Bell",
    "website": "http://www.yourcompany.com",
    "version": "1.2.3",
    "depends": [
        "base",
        "account_accountant",
        "purchase_requisition",
        "hr_payroll_account",
    ],
    "data": [
        # 'security/ir.model.access.csv',
        "security/res_group.xml",
        "views/account_move.xml",
        "views/actions.xml",
        "views/hr_payslip_run.xml",
        "data/mail_template.xml",
    ],
    "license": "LGPL-3",
}
