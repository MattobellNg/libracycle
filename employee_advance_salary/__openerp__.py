# -*- coding: utf-8 -*-

# Part of Probuse Consulting Service Pvt Ltd. See LICENSE file for full copyright and licensing details.

{
    "name": "Employee Advance Salary Requests",
    "version": "1.0",
    "price": 49.0,
    "currency": "EUR",
    "license": "Other proprietary",
    "category": "Human Resources",
    "summary": "Employee Advance Salary Requests and Workflow - Integrated with Accounting",
    "description": """
        Employee Advance Salary Requests:

Employee advance salary
advance salary
salary advance
advance employee
salary advance
employee advance
salary request
advance request
payroll salary
accounting salary
Salary Advances
Salary Advance
Employee Cash Advances
Employee Cash Advance
employee_advance_salary
employee advance salary process
director salary approval
advance request
cash advance
employee cash advance
salary in advance
employee salary
hr payroll
payroll employee
employee hr payroll
payroll
            """,
    "author": "Probuse Consulting Service Pvt. Ltd.",
    "website": "www.probuse.com",
    "depends": ["hr", "account", "hr_payroll"],
    "data": [
        "security/employee_advance_salary_security.xml",
        "security/ir.model.access.csv",
        "data/salary_rule_data.xml",
        "views/employee_advance_salary.xml",
        "views/hr_job.xml",
        "report/employee_advance_salary_report.xml",
    ],
    "installable": True,
    "application": False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
