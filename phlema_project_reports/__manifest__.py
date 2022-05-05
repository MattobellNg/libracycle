# License: Odoo Proprietary License v1.0

{
    "name": "Dynamic Project Reports - PDF, Excel",
    "version": "10.0",
    "category": "Project Management",
    "summary": "All in One Dynamic Project Reports For" " Odoo & Export the Report in PDF or Excel",
    "sequence": "10",
    "author": "Ailemen Stephen U",
    "license": "OPL-1",
    "maintainer": "Ailemen Stephen U",
    "support": "phlemaconcept@gmail.com",
    "website": "",
    "depends": ["project_description", "phlema_project_stock"],
    "demo": [],
    "data": [
        "views/report_templates.xml",
        "views/dynamic_project_reports.xml",
        "report/report_ph_project_pdf.xml",
        "report/reports.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["static/description/banner.gif"],
    "qweb": ["static/src/xml/*.xml"],
}
