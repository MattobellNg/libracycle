from odoo import fields, models, api


class ProjectprojectExtension(models.Model):
    _inherit = "project.project"

    delivery_count = fields.Integer(compute="_compute_delivery_count", string="Tasks")
    item_delivery_count = fields.Integer(compute="_compute_delivered_count", string="Delivered Count")
    item_awaiting_delivery_count = fields.Integer(
        compute="_compute_awaiting_delivery_count", string="Item Awaiting Delivery"
    )
    project_delivery_ids = fields.One2many("stock.picking", "project_id", "Delivery Process")
    container_move_ids = fields.One2many("project.container.movement", "project_id", "Container Move")
    container_return_count = fields.Integer(compute="_compute_container_return_count", string="Container Count")

    def _compute_container_return_count(self):
        for container in self:
            container.container_return_count = len(container.container_move_ids)

    def _compute_delivery_count(self):
        for delv in self:
            delv.delivery_count = len(delv.project_delivery_ids)

    def _compute_delivered_count(self):
        for delv in self:
            schedule_item = delv.project_schedule_items_ids.filtered(
                lambda r: r.stock_delivery_state in ["dispatch", "delivered"]
            )
            delv.item_delivery_count = len(schedule_item)

    def _compute_awaiting_delivery_count(self):
        for delv in self:
            sched_items = delv.project_schedule_items_ids.filtered(
                lambda r: r.stock_delivery_state in ["in_transit", "draft", "prepare"]
            )
            delv.item_awaiting_delivery_count = len(sched_items)

    def action_delivered(self):
        for proj in self:
            schedule_item = 0
            total_items = 0
            if proj.project_schedule_items_ids:
                total_items = len(proj.project_schedule_items_ids)
            if proj.item_delivery_count:
                schedule_item = proj.item_delivery_count
            if total_items >= schedule_item and proj.state in ["pending", "progress"]:
                proj.write({"state": "deliver"})

    def action_view_delivery(self):
        self.ensure_one()
        action = self.env.ref("stock.action_picking_tree")

        return {
            "name": action.name,
            "help": action.help,
            "type": action.type,
            "view_type": action.view_type,
            "view_mode": action.view_mode,
            "target": action.target,
            "context": "{}",
            "res_model": action.res_model,
            "domain": [("project_id", "=", self.id)],
        }

    def action_view_returned_container(self):
        self.ensure_one()
        action = self.env.ref("phlema_project_stock.project_container_movement_act_window")

        return {
            "name": action.name,
            "help": action.help,
            "type": action.type,
            "view_type": action.view_type,
            "view_mode": action.view_mode,
            "target": action.target,
            "context": {"default_project_id": self.id},
            "res_model": action.res_model,
            "domain": [("project_id", "=", self.id)],
        }
