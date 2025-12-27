from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import logging

_logger = logging.getLogger(__name__)

class ProjectApprovalRequest(models.Model):
    _name = 'project.approval.request'
    _description = 'Project Approval Request'
    _order = 'create_date desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Request Number',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('New')
    )
    
    project_id = fields.Many2one(
        'project.project',
        string='Project',
        required=True,
        ondelete='cascade',
        tracking=True
    )
    
    requested_by = fields.Many2one(
        'res.users',
        string='Requested By',
        required=True,
        default=lambda self: self.env.user,
        tracking=True
    )
    
    approved_by = fields.Many2one(
        'res.users',
        string='Approved By',
        readonly=True,
        tracking=True
    )
    
    approved_date = fields.Datetime(
        string='Approved Date',
        readonly=True,
        tracking=True
    )
    
    rejected_by = fields.Many2one(
        'res.users',
        string='Rejected By',
        readonly=True,
        tracking=True
    )
    
    rejected_date = fields.Datetime(
        string='Rejected Date',
        readonly=True,
        tracking=True
    )
    
    reason = fields.Text(
        string='Reason',
        required=True,
        tracking=True
    )
    
    approval_notes = fields.Text(
        string='Approval Notes',
        tracking=True
    )
    
    rejection_reason = fields.Text(
        string='Rejection Reason',
        tracking=True
    )
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)
    
    # Computed fields
    project_name = fields.Char(
        string='Project Name',
        related='project_id.name',
        store=True
    )
    
    project_partner = fields.Many2one(
        'res.partner',
        string='Project Partner',
        related='project_id.partner_id',
        store=True
    )

    @api.model
    def create(self, vals):
        """Override create to generate sequence number"""
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('project.approval.request') or _('New')
        return super().create(vals)

    def action_submit(self):
        """Submit the approval request"""
        self.ensure_one()
        
        if self.state != 'draft':
            raise UserError(_("Only draft requests can be submitted."))
        
        if not self.reason:
            raise UserError(_("Please provide a reason for the approval request."))
        
        self.state = 'pending'
        self._notify_approvers()
        
        self.message_post(
            body=_("Approval request submitted for review."),
            message_type='comment'
        )

    def action_approve(self):
        """Approve the request"""
        self.ensure_one()
        
        if self.state != 'pending':
            raise UserError(_("Only pending requests can be approved."))
        
        if not self.env.user.has_group('project_approval_workflow.group_project_approver'):
            raise UserError(_("You don't have permission to approve this request."))
        
        self.write({
            'state': 'approved',
            'approved_by': self.env.user.id,
            'approved_date': fields.Datetime.now(),
        })
        
        # Unlock the project's analytic account
        if self.project_id.analytic_account_locked:
            self.project_id.analytic_account_locked = False
        
        self.message_post(
            body=_("Request approved by %s") % self.env.user.name,
            message_type='comment'
        )
        
        # Notify the requester
        self._notify_requester('approved')

    def action_reject(self):
        """Reject the request"""
        self.ensure_one()
        
        if self.state != 'pending':
            raise UserError(_("Only pending requests can be rejected."))
        
        if not self.env.user.has_group('project_approval_workflow.group_project_approver'):
            raise UserError(_("You don't have permission to reject this request."))
        
        if not self.rejection_reason:
            raise UserError(_("Please provide a reason for rejection."))
        
        self.write({
            'state': 'rejected',
            'rejected_by': self.env.user.id,
            'rejected_date': fields.Datetime.now(),
        })
        
        self.message_post(
            body=_("Request rejected by %s. Reason: %s") % (
                self.env.user.name, self.rejection_reason
            ),
            message_type='comment'
        )
        
        # Notify the requester
        self._notify_requester('rejected')

    def action_cancel(self):
        """Cancel the request"""
        self.ensure_one()
        
        if self.state not in ['draft', 'pending']:
            raise UserError(_("Only draft or pending requests can be cancelled."))
        
        if self.state == 'pending' and self.requested_by != self.env.user:
            if not self.env.user.has_group('project_approval_workflow.group_project_approver'):
                raise UserError(_("You don't have permission to cancel this request."))
        
        self.state = 'cancelled'
        
        self.message_post(
            body=_("Request cancelled by %s") % self.env.user.name,
            message_type='comment'
        )

    def action_reset_to_draft(self):
        """Reset the request to draft"""
        self.ensure_one()
        
        if self.state not in ['rejected', 'cancelled']:
            raise UserError(_("Only rejected or cancelled requests can be reset to draft."))
        
        if self.requested_by != self.env.user:
            raise UserError(_("Only the requester can reset the request to draft."))
        
        self.write({
            'state': 'draft',
            'approved_by': False,
            'approved_date': False,
            'rejected_by': False,
            'rejected_date': False,
            'approval_notes': False,
            'rejection_reason': False,
        })
        
        self.message_post(
            body=_("Request reset to draft by %s") % self.env.user.name,
            message_type='comment'
        )

    def _notify_approvers(self):
        """Send notification to approvers"""
        approvers = self.env['res.users'].search([
            ('groups_id', 'in', self.env.ref('project_approval_workflow.group_project_approver').id)
        ])
        
        for approver in approvers:
            self.env['mail.activity'].create({
                'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                'note': _('New approval request for project %s') % self.project_id.name,
                'res_id': self.id,
                'res_model_id': self.env['ir.model']._get('project.approval.request').id,
                'user_id': approver.id,
                'summary': _('Project Approval Request'),
            })

    def _notify_requester(self, action):
        """Send notification to requester about approval/rejection"""
        subject = _('Approval Request %s') % action.title()
        body = _('Your approval request for project %s has been %s.') % (
            self.project_id.name, action
        )
        
        if action == 'rejected' and self.rejection_reason:
            body += _('\n\nRejection reason: %s') % self.rejection_reason
        
        self.env['mail.activity'].create({
            'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
            'note': body,
            'res_id': self.requested_by.id,
            'res_model_id': self.env['ir.model']._get('res.users').id,
            'user_id': self.requested_by.id,
            'summary': subject,
        })

    @api.constrains('project_id', 'state')
    def _check_unique_pending_request(self):
        """Ensure only one pending request per project"""
        for record in self:
            if record.state == 'pending':
                existing_pending = self.search([
                    ('project_id', '=', record.project_id.id),
                    ('state', '=', 'pending'),
                    ('id', '!=', record.id)
                ])
                if existing_pending:
                    raise ValidationError(_(
                        "There is already a pending approval request for this project. "
                        "Please wait for the current request to be processed."
                    )) 