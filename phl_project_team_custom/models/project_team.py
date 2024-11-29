from odoo import models, api

class PhlProjectProject(models.Model):
    _inherit = "project.project"

    def _get_users_to_project_subscribe(self, project=False):
        partner_ids = self.env["res.partner"]
        project = project or self
        if project.user_id:
            partner_ids |= project.user_id.partner_id
        if project.members:
            partner_ids |= project.members.mapped("partner_id")
        
        # Filter out customer partners only
        partner_ids = partner_ids.filtered(lambda partner: not partner.customer_rank)
        
        return partner_ids
