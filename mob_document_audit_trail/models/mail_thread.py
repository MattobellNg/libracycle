from odoo import models, fields, api

class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'
    
    def _message_post_after_hook(self, message, msg_vals):
        """Override to enhance attachment display in chatter"""
        res = super()._message_post_after_hook(message, msg_vals)
        
        # Add upload info to attachment messages
        if message.attachment_ids:
            for attachment in message.attachment_ids:
                if hasattr(attachment, 'uploaded_by') and attachment.uploaded_by:
                    # The upload info is already posted via _post_attachment_message
                    pass
                    
        return res

    def action_view_upload_history(self):
        """Action to view upload history (can be extended with mail.thread)"""
        return {
            'name': 'Upload History',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'ir.attachment',
            'res_id': self.id,
            'target': 'new',
            'context': {'create': False, 'edit': False}
        }