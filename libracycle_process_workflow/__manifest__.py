{
    "name": "Libra Payment Process Flow",
    "summary": """Libra Payment Process Flow""",
    "description": """
        Libra Payment Process Flow
    """,
    "author": "Matt O'Bell",
    "website": "http://www.yourcompany.com",
    "version": "1.2.5",
    "depends": [
        "base",
        "account_accountant",
        "purchase_requisition",
        "hr_payroll_account",
        "sale_management",
        "analytic_enterprise",
        "sale_project",
    ],
    "data": [
        # 'security/ir.model.access.csv',
        "security/res_group.xml",
        "views/account_move.xml",
        "views/res_partner.xml",
        "data/ir_sequence.xml",
        "views/hr_payslip_run.xml",
        "views/sale_order.xml",
        "data/mail_template.xml",
        "report/report_saleorder.xml",
    ],
    "license": "LGPL-3",
}
