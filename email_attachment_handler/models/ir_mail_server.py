from odoo import models, fields, api
import base64

class CustomIrMailServer(models.Model):
    _inherit = 'ir.mail_server'
    
    def build_email(self, email_from, email_to, subject, body, email_cc=None, email_bcc=None, reply_to=False,
                   attachments=None, message_id=None, references=None, object_id=None, subtype='plain', headers=None,
                   body_alternative=None, subtype_alternative='plain'):
        
        if attachments:
            new_body = body
            if isinstance(new_body, bytes):
                new_body = new_body.decode()
            
            stored_attachments = []
            for attachment in attachments:
                name, content, mime = attachment
                
                # Store attachment in Odoo filestore
                stored_attachment = self.env['attachment.store'].create({
                    'name': name,
                    'datas': base64.b64encode(content),
                    'mimetype': mime,
                })
                
                # Generate download link
                download_url = stored_attachment.get_download_url()
                
                # Add link to email body
                link_html = f'<p>Attachment: <a href="{download_url}">{name}</a></p>'
                if subtype == 'html':
                    new_body += link_html
                else:
                    new_body += f"\nAttachment: {name}\nDownload link: {download_url}\n"
            
            return super(CustomIrMailServer, self).build_email(
                email_from=email_from,
                email_to=email_to,
                subject=subject,
                body=new_body,
                email_cc=email_cc,
                email_bcc=email_bcc,
                reply_to=reply_to,
                attachments=[],  # Empty list as we've handled the attachments
                message_id=message_id,
                references=references,
                object_id=object_id,
                subtype=subtype,
                headers=headers,
                body_alternative=body_alternative,
                subtype_alternative=subtype_alternative
            )
        
        return super(CustomIrMailServer, self).build_email(
            email_from=email_from,
            email_to=email_to,
            subject=subject,
            body=body,
            email_cc=email_cc,
            email_bcc=email_bcc,
            reply_to=reply_to,
            attachments=attachments,
            message_id=message_id,
            references=references,
            object_id=object_id,
            subtype=subtype,
            headers=headers,
            body_alternative=body_alternative,
            subtype_alternative=subtype_alternative
        )