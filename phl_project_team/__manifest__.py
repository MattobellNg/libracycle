# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Project Team",
    "author": "Serpent Consulting Services Pvt. Ltd.",
    "summary": "Adds Project Team Members.",
    "category": "Project Management.",
    "website": "http://www.serpentcs.com",
    "version": "1.0.1",
    "sequence": 1,
    "depends": ["project", "crm"],
    "data": ["security/project_team_security.xml", "views/project_team_view.xml"],
    "installable": True,
    "auto_install": False,
}
