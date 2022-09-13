from urllib.parse import urlencode, urljoin

from odoo import api, fields, models
from odoo.exceptions import ValidationError

class AccountMove(models.Model):
    _inherit = "account.move"

    state = fields.Selection(
        selection_add=[
            ("officer", "Officer"),
            ("qac", "QAC"),
            ("review", "Reviewed"),
            ("posted",),
        ],
        ondelete={
            "officer": lambda m: m.write({"state": "draft"}),
            "qac": lambda m: m.write({"state": "draft"}),
            "review": lambda m: m.write({"state": "draft"}),
        },
    )

    bank_account_id = fields.Many2one('res.bank.account', string='Bank Account',  required=False)
    invoice_date = fields.Date(string='Invoice/Bill Date', readonly=True, index=True, copy=False,states={})

    def action_post(self):
        res = super(AccountMove,self).action_post()
        if self.move_type =='in_invoice':
            self.broadcast_notification_qac()
        return res


    @api.model_create_multi
    def create(self, vals_list):
        res =  super(AccountMove, self).create(vals_list)
        if res.move_type=='in_invoice':
            res.broadcast_notification()

        return res

    def action_submit(self):
        for rec in self:
            if rec.partner_id:
                rec.write({"state": "officer"})
            else:
                raise ValidationError("Add a partner to the bill")

    def action_officer_approve(self):
        for rec in self:
            rec.broadcast_notification_qac()
            rec.write({"state": "qac"})



    def action_qac_approve(self):
        for rec in self:
            
            rec.write({'state': 'review'})

    def action_reject(self):
        for rec in self:
            rec.write({'state': 'draft'})

    def broadcast_notification_qac(self):
        url = self.request_link()
        email_from = self.env.user.partner_id.email
        recipients = users = "".join(
        self.env.ref("libracycle_process_workflow.group_qac").users.mapped(
                    "email"
                )
            )
        mail_template = self.env.ref(
                "libracycle_process_workflow.mail_template_approved"
            )
        mail_template.with_context(
                {
                    "recipient": recipients,
                    "url": url,
                    "email_from": email_from,
                    "title": self.env.user.name,
                }
            ).send_mail(self.id, force_send=False)

    def broadcast_notification(self):
        recipients = []

        url = self.request_link()
        partner_ids_1 = self.env.ref("account.group_account_manager").users.mapped('email')
        partner_ids_2 = self.env.ref("libracycle_process_workflow.group_qac").users.mapped('email')
        partner_ids_3 = self.env.ref("libracycle_process_workflow.group_officer").users.mapped('email')
        recipients.extend(partner_ids_1)
        recipients.extend(partner_ids_2)
        recipients.extend(partner_ids_3)
        recipients = ", ".join(recipients)

  
        email_from = self.env.user.partner_id.email
        mail_template = self.env.ref(
                "libracycle_process_workflow.libracycle_mail_template_move"
            )
        mail_template.with_context(
                {
                    "recipient": recipients,
                    "url": url,
                    "email_from": email_from,
                    "title": self.env.user.name,
                }
            ).send_mail(self.id, force_send=False)
  

    def request_link(self):
        fragment = {}
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
        fragment.update(model=self._name, view_type="form", db=self.env.cr.dbname)
        return urljoin(base_url, "/web?#id=%s&%s" % (self.id, urlencode(fragment)))

 


