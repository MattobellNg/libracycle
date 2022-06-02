# © 2016-2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Project Configurable Category",
    "version": "10.0.2.2.1",
    "category": "Project Management",
    "website": "https://www.elico-corp.com",
    "support": "support@elico-corp.com",
    "author": "Elico corp",
    "license": "AGPL-3",
    "depends": ["project", "project_category", "project_description"],
    "data": [
        "data/project_project_category_data.xml",
        "security/ir.model.access.csv",
        "views/project_project_view.xml",
        "views/project_task_views.xml",
        "views/project_project_category_view.xml",
    ],
    "installable": True,
}
