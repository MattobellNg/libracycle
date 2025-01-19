import base64
import hmac
import logging
from io import BytesIO
from odoo import http
from odoo.http import request, Response
from odoo.exceptions import AccessError, ValidationError
from werkzeug.exceptions import NotFound, BadRequest

_logger = logging.getLogger(__name__)

class AttachmentController(http.Controller):
    @http.route('/attachment/download/<int:attachment_id>/<string:access_token>', 
                type='http', auth='public', csrf=False)
    def download_attachment(self, attachment_id, access_token, **kwargs):
        try:
            if not attachment_id or not access_token:
                raise BadRequest("Missing required parameters")

            # Use proper model name and add exists() check
            attachment = request.env['attachment.store'].sudo().browse(attachment_id)
            if not attachment.exists():
                _logger.warning(f"Attachment not found: {attachment_id}")
                raise NotFound("Attachment not found")
            
            # Validate access token with constant-time comparison
            if not self._check_access_token(attachment, access_token):
                _logger.warning(f"Invalid access token for attachment: {attachment_id}")
                raise AccessError("Invalid access token")
            
            if not attachment.datas:
                raise ValidationError("Attachment contains no data")
                
            if not attachment.datas:
                raise ValidationError("Attachment contains no data")
                
            # Convert binary data to file-like object
            file_data = BytesIO(base64.b64decode(attachment.datas))
                
            return http.send_file(
                file_data,
                filename=attachment.name,
                mimetype=attachment.mimetype or 'application/octet-stream',
                as_attachment=True
            )

        except (AccessError, ValidationError) as e:
            _logger.error(f"Access error downloading attachment {attachment_id}: {str(e)}")
            return Response(status=403, response=str(e))
            
        except NotFound as e:
            return request.not_found()
            
        except BadRequest as e:
            return Response(status=400, response=str(e))
            
        except Exception as e:
            _logger.exception(f"Error downloading attachment {attachment_id}")
            return Response(status=500, response="Internal server error")

    def _check_access_token(self, attachment, token):
        """Helper method to check access token in constant time"""
        if not attachment.access_token or not token:
            return False
        return hmac.compare_digest(attachment.access_token, token)