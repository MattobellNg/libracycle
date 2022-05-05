from odoo import fields, models, api


class ProjectSalesOrder(models.Model):
    _inherit = "sale.order"

    project_items_ids = fields.One2many(
        "project.schedule.items",
        "project_order_id",
        "Project Items",
        domain=lambda self: [("project_id", "=", self.project_project_id.id)],
    )

    job_id = fields.Many2one("project.project", string="Job ID")
