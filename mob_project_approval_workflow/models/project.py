from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import logging

_logger = logging.getLogger(__name__)

class ProjectProject(models.Model):
    _inherit = 'project.project'

    # Basic locking field
    analytic_account_locked = fields.Boolean(
        string='Analytic Account Locked',
        default=False,
        help='Indicates if the analytic account is locked due to post-delivery state'
    )

    @api.onchange('sn_state')
    def _onchange_sn_state(self):
        """Handle state changes and automatic actions"""
        super()._onchange_sn_state()
        
        if self.sn_state == 'post_delivery':
            # Automatically set status_delivered to True
            if not self.status_delivered:
                self.status_delivered = True
                self.message_post(
                    body=_("Project automatically marked as delivered due to post-delivery state."),
                    message_type='comment'
                )
            
            # Lock the analytic account
            if not self.analytic_account_locked:
                self.analytic_account_locked = True
                self.message_post(
                    body=_("Analytic account has been locked due to post-delivery state."),
                    message_type='comment'
                )

    def write(self, vals):
        """Override write to handle analytic account locking"""
        # Check if trying to modify analytic account when locked
        if 'analytic_account_id' in vals and self.analytic_account_locked:
            raise UserError(_(
                "Cannot modify the analytic account while it is locked. "
                "The analytic account is locked due to post-delivery state."
            ))
        
        result = super().write(vals)
        
        # Handle state changes after write
        for project in self:
            if 'sn_state' in vals and vals['sn_state'] == 'post_delivery':
                project._handle_post_delivery_state()
        
        return result

    def _handle_post_delivery_state(self):
        """Handle actions when project reaches post-delivery state"""
        if not self.status_delivered:
            self.status_delivered = True
            self.message_post(
                body=_("Project automatically marked as delivered due to post-delivery state."),
                message_type='comment'
            )
        
        if not self.analytic_account_locked:
            self.analytic_account_locked = True
            self.message_post(
                body=_("Analytic account has been locked due to post-delivery state."),
                message_type='comment'
            )

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        """Override to make analytic account readonly when locked"""
        result = super().fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        
        if view_type == 'form':
            # Get the current record if we're editing
            active_id = self._context.get('active_id')
            if active_id:
                project = self.browse(active_id)
                if project.analytic_account_locked:
                    # Make analytic_account_id readonly when locked
                    import xml.etree.ElementTree as ET
                    arch = ET.fromstring(result['arch'])
                    
                    for field in arch.findall(".//field[@name='analytic_account_id']"):
                        field.set('readonly', '1')
                    
                    result['arch'] = ET.tostring(arch, encoding='unicode')
        
        return result 