from odoo import models, fields, api
from odoo.http import request
from markupsafe import Markup
import logging

_logger = logging.getLogger(__name__)

class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    # Upload tracking fields
    uploaded_by = fields.Many2one('res.users', string='Uploaded By', readonly=True)
    upload_date = fields.Datetime(string='Upload Date', readonly=True)
    upload_ip = fields.Char(string='Upload IP Address', readonly=True)
    
    # Modification tracking fields
    last_modified_by = fields.Many2one('res.users', string='Last Modified By', readonly=True)
    last_modified_date = fields.Datetime(string='Last Modified Date', readonly=True)
    modification_count = fields.Integer(string='Modification Count', default=0, readonly=True)
    
    # Additional tracking fields
    file_hash = fields.Char(string='File Hash', readonly=True, help="SHA256 hash of the file content")
    original_filename = fields.Char(string='Original Filename', readonly=True)
    file_size_human = fields.Char(string='File Size', compute='_compute_file_size_human', store=True)

    @api.depends('file_size')
    def _compute_file_size_human(self):
        """Convert file size to human readable format"""
        for record in self:
            if record.file_size:
                size = record.file_size
                for unit in ['B', 'KB', 'MB', 'GB']:
                    if size < 1024.0:
                        record.file_size_human = f"{size:.1f} {unit}"
                        break
                    size /= 1024.0
                else:
                    record.file_size_human = f"{size:.1f} TB"
            else:
                record.file_size_human = "0 B"

    def _get_client_ip(self):
        """Get client IP address from request"""
        if request:
            return request.httprequest.environ.get('HTTP_X_FORWARDED_FOR', 
                   request.httprequest.environ.get('REMOTE_ADDR', 'Unknown'))
        return 'System'

    def _compute_file_hash(self, data):
        """Compute SHA256 hash of file content"""
        import hashlib
        if data:
            return hashlib.sha256(data).hexdigest()
        return False

    @api.model_create_multi
    def create(self, vals_list):
        """Override create to track upload information"""
        for vals in vals_list:
            # Set upload tracking fields
            vals['uploaded_by'] = self.env.user.id
            vals['upload_date'] = fields.Datetime.now()
            vals['upload_ip'] = self._get_client_ip()
            vals['last_modified_by'] = self.env.user.id
            vals['last_modified_date'] = fields.Datetime.now()
            vals['modification_count'] = 0
            
            # Store original filename if not already set
            if 'name' in vals and not vals.get('original_filename'):
                vals['original_filename'] = vals['name']
            
            # Compute file hash if datas is provided
            if 'datas' in vals and vals['datas']:
                import base64
                try:
                    file_data = base64.b64decode(vals['datas'])
                    vals['file_hash'] = self._compute_file_hash(file_data)
                except Exception as e:
                    _logger.warning(f"Could not compute file hash: {e}")
        
        attachments = super().create(vals_list)
        
        # Post message to chatter for attachments linked to records
        for attachment in attachments:
            _logger.info(f"Attachment created: {attachment.name}, res_model: {attachment.res_model}, res_id: {attachment.res_id}")
            if attachment.res_model and attachment.res_id:
                try:
                    attachment._post_attachment_message()
                    _logger.info(f"Successfully posted attachment message for {attachment.name}")
                except Exception as e:
                    _logger.error(f"Failed to post attachment message for {attachment.name}: {e}")
            else:
                _logger.info(f"Skipping message post for {attachment.name} - no res_model or res_id")
        
        return attachments

    def _post_attachment_message(self):
        """Post a message to the chatter about the document upload"""
        if not (self.res_model and self.res_id):
            _logger.info(f"No res_model or res_id for attachment {self.name}")
            return
            
        try:
            record = self.env[self.res_model].browse(self.res_id)
            _logger.info(f"Found record: {record} of type {self.res_model}")
            
            if hasattr(record, 'message_post'):
                upload_time = fields.Datetime.to_string(self.upload_date)
                # Get file size with fallback
                file_size_display = self.file_size_human or f"{self.file_size} bytes" if self.file_size else "Unknown"
                
                # message_body = Markup(f"""
                # <div class="o_mail_thread_message_attachment_info">
                #     <strong>📎 Document Upload Information</strong><br/>
                #     <ul>
                #         <li><strong>File:</strong> {self.name}</li>
                #         <li><strong>Size:</strong> {file_size_display}</li>
                #         <li><strong>Uploaded by:</strong> {self.uploaded_by.name}</li>
                #         <li><strong>Upload time:</strong> {upload_time}</li>
                #     </ul>
                # </div>
                # """)
                
                _logger.info(f"Posting message to {self.res_model} #{self.res_id}")
                result = record.message_post(
                    body="",
                    message_type='comment',
                    subtype_xmlid='mail.mt_comment',
                    attachment_ids=[self.id]
                )
                _logger.info(f"Message posted successfully: {result}")
            else:
                _logger.warning(f"Record {record} does not have message_post method")
        except Exception as e:
            _logger.error(f"Could not post attachment message: {e}", exc_info=True)

    def write(self, vals):
        """Override write to track modification information"""
        # Check if this is a content modification
        content_fields = ['datas', 'name', 'description']
        is_content_modification = any(field in vals for field in content_fields)
        
        if is_content_modification:
            vals['last_modified_by'] = self.env.user.id
            vals['last_modified_date'] = fields.Datetime.now()
            
            # Increment modification count
            for record in self:
                vals['modification_count'] = record.modification_count + 1
            
            # Update file hash if datas is being modified
            if 'datas' in vals and vals['datas']:
                import base64
                try:
                    file_data = base64.b64decode(vals['datas'])
                    vals['file_hash'] = self._compute_file_hash(file_data)
                except Exception as e:
                    _logger.warning(f"Could not compute file hash: {e}")
        
        return super().write(vals)

    @api.model
    def create_retroactive_attachment_comments(self):
        """Create comments for all existing attachments that don't have upload tracking"""
        _logger.info("Starting retroactive attachment comment creation...")
        
        # Find all attachments that have res_model and res_id but no upload tracking
        attachments = self.search([
            ('res_model', '!=', False),
            ('res_id', '!=', False),
            '|',
            ('uploaded_by', '=', False),
            ('upload_date', '=', False)
        ])
        
        _logger.info(f"Found {len(attachments)} attachments without upload tracking")
        
        created_count = 0
        error_count = 0
        
        for attachment in attachments:
            try:
                # Check if a comment already exists for this attachment
                record = self.env[attachment.res_model].browse(attachment.res_id)
                if hasattr(record, 'message_ids'):
                    existing_messages = record.message_ids.filtered(
                        lambda m: m.attachment_ids and attachment.id in m.attachment_ids.ids
                    )
                    
                    if existing_messages:
                        _logger.info(f"Skipping {attachment.name} - comment already exists")
                        continue
                
                # Create retroactive comment
                self._create_retroactive_attachment_message(attachment)
                created_count += 1
                
                if created_count % 10 == 0:  # Log progress every 10 attachments
                    _logger.info(f"Processed {created_count} attachments...")
                    
            except Exception as e:
                _logger.error(f"Error processing attachment {attachment.name}: {e}")
                error_count += 1
        
        _logger.info(f"Retroactive comment creation completed. Created: {created_count}, Errors: {error_count}")
        return {
            'created': created_count,
            'errors': error_count,
            'total_processed': len(attachments)
        }

    def _create_retroactive_attachment_message(self, attachment):
        """Create a retroactive message for an existing attachment"""
        if not (attachment.res_model and attachment.res_id):
            return
            
        try:
            record = self.env[attachment.res_model].browse(attachment.res_id)
            if not hasattr(record, 'message_post'):
                return
            
            # Use create_date as upload time if available, otherwise use current time
            upload_time = attachment.create_date or fields.Datetime.now()
            
            # Get file size with fallback
            file_size_display = attachment.file_size_human or f"{attachment.file_size} bytes" if attachment.file_size else "Unknown"
            
            # Determine who uploaded (use creator if available, otherwise system)
            uploaded_by_name = "System"
            if attachment.create_uid:
                uploaded_by_name = attachment.create_uid.name
            
            # message_body = Markup(f"""
            # <div class="o_mail_thread_message_attachment_info">
            #     <strong>📎 Document Upload Information (Retroactive)</strong><br/>
            #     <ul>
            #         <li><strong>File:</strong> {attachment.name}</li>
            #         <li><strong>Size:</strong> {file_size_display}</li>
            #         <li><strong>Uploaded by:</strong> {uploaded_by_name}</li>
            #         <li><strong>Upload time:</strong> {fields.Datetime.to_string(upload_time)}</li>
            #         <li><strong>Note:</strong> This comment was created retroactively</li>
            #     </ul>
            # </div>
            # """)
            
            # Create the message with the original upload time
            record.with_context(mail_create_nosubscribe=True).message_post(
                body="",
                message_type='comment',
                subtype_xmlid='mail.mt_comment',
                attachment_ids=[attachment.id],
                # Use the original creation time for the message
                create_date=upload_time
            )
            
            _logger.info(f"Created retroactive comment for attachment {attachment.name}")
            
        except Exception as e:
            _logger.error(f"Could not create retroactive message for {attachment.name}: {e}", exc_info=True)
            raise