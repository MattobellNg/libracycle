{
    "name": "Libra Payment Process Flow",
    "summary": """Libra Payment Process Flow""",
    "description": """
        Libra Payment Process Flow
    """,
    "author": "Matt O'Bell",
    "website": "http://www.yourcompany.com",
    "version": "1.3.0",
    "depends": [
        "sale",
        "account_accountant",
        "purchase_requisition",
        "hr_payroll_account",
        "sale_management",
        "analytic_enterprise",
        "sale_project",
        "hr_expense",
        "customize_vpcs"
    ],
    "data": [
        'security/ir.model.access.csv',
        "security/res_group.xml",
        "views/account_move.xml",
        "views/res_partner.xml",
        "views/project_project.xml",
        "data/ir_sequence.xml",
        "views/hr_payslip_run.xml",
        "views/sale_order.xml",
        "views/res_bank_account.xml",
        "views/hr_expense_sheet.xml",
        "data/mail_template.xml",
        "report/report_saleorder.xml",
    ],
    "license": "LGPL-3",
}
