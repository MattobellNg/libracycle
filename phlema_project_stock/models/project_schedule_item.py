from odoo import fields, models, api


class ProjectContainerMovement(models.Model):
    _name = "project.container.movement"
    _description = "This container movement"

    project_id = fields.Many2one("project.project", "Project")
    item_id = fields.Many2one(
        "project.schedule.items",
        "Container List",
        domain="[('project_id', '=', project_id),('stock_delivery_state', '=', 'dispatch')]",
    )

    name = fields.Char("Container number", related="item_id.name")
    current_location_id = fields.Many2one("stock.location", "From", required=True)
    destination_location_id = fields.Many2one("stock.location", "To", required=True)
    movement_date = fields.Date("Movement date")
    arrived_date = fields.Date("Arrived date")


class ProjectScheduleItemExt(models.Model):
    _inherit = "project.schedule.items"

    stock_move_id = fields.Many2one("stock.move", "Delivery")
    stock_delivery_state = fields.Selection(related="stock_move_id.delivery_status", store=True)
    is_container = fields.Boolean("Container flag", default=False)
