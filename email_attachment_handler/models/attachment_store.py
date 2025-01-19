from odoo import models, fields, api
from werkzeug.urls import url_join
import hashlib
from datetime import datetime

class AttachmentStore(models.Model):
    _name = 'attachment.store'
    _description = 'Stored Email Attachments'

    name = fields.Char('Name', required=True)
    datas = fields.Binary('File Content', attachment=True)
    mimetype = fields.Char('Mime Type')
    create_date = fields.Datetime('Created On', readonly=True)
    access_token = fields.Char('Access Token', readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        # Generate access token for each attachment
        for vals in vals_list:
            vals['access_token'] = hashlib.sha256(
                f"{fields.Datetime.now()}{vals.get('name')}".encode()
            ).hexdigest()
        return super().create(vals_list)

    def get_download_url(self):
        self.ensure_one()
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        return url_join(base_url, f'/attachment/download/{self.id}/{self.access_token}')