{
    "name": "Project Stock",
    "version": "10.0.01",
    "summary": "This module handles project or job stock",
    "description": "Description",
    "category": "Warehouse",
    "author": "Ailemen Stephen U.",
    "license": "AGPL-3",
    "depends": [
        "base",
        "project",
        "stock",
        "sale_stock",
        "project_description",
        "project_project_category",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/res_partner.xml",
        "views/stock_move_views.xml",
        "views/stock_picking_view.xml",
        "views/project_view.xml",
        "views/stock_pack_operation_view.xml",
        "views/project_schedule_item_view.xml",
        "views/stock_pack_sub_operation.xml",
        "views/container_returned_view.xml",
    ],
    "demo": [],
    "installable": True,
    "auto_install": False,
}
