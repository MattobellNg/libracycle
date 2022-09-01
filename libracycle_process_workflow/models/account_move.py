from urllib.parse import urlencode, urljoin

from odoo import api, fields, models
from odoo.exceptions import ValidationError

class AccountMove(models.Model):
    _inherit = "account.move"

    state = fields.Selection(
        selection_add=[
            ("officer", "Officer"),
            ("qac", "QAC"),
            ("posted",),
        ],
        ondelete={
            "officer": lambda m: m.write({"state": "draft"}),
            "qac": lambda m: m.write({"state": "draft"}),
        },
    )

    bank_account_id = fields.Many2one('res.bank.account', string='Bank Account',  required=False)

    def action_submit(self):
        for rec in self:
            if rec.partner_id:
                url = self.request_link()
                email_from = self.env.user.partner_id.email
                recipients = users = "".join(
                    self.env.ref(
                        "libracycle_process_workflow.group_officer"
                    ).users.mapped("email")
                )
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
                rec.write({"state": "officer"})
            else:
                raise ValidationError("Add a partner to the bill")

    def action_officer_approve(self):
        for rec in self:
            url = self.request_link()
            email_from = self.env.user.partner_id.email
            recipients = users = "".join(
                self.env.ref("libracycle_process_workflow.group_qac").users.mapped(
                    "email"
                )
            )
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
            rec.write({"state": "qac"})



    def action_qac_approve(self):
        for rec in self:
            rec.action_post()

    def action_reject(self):
        for rec in self:
            rec.write({'state': 'draft'})

    def send_notification(self, body, subject, group, email_from):
        partner_ids = []


        users = self.env.ref(group).users
        for user in users:
            partner_ids.append(user.partner_id.id)

        if partner_ids:
            self.message_post(
                body=body,
                email_from=email_from,
                subject=subject,
                partner_ids=partner_ids,
                message_type="email",
                notify_by_email=True,
            )
        return True

    def request_link(self):
        fragment = {}
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
        fragment.update(base_url=base_url)
        fragment.update(model=self._name)
        fragment.update(view_type="form")
        fragment.update(id=self.id)
        query = {"db": self.env.cr.dbname}
        res = urljoin(base_url, "?%s#%s" % (urlencode(query), urlencode(fragment)))
        return res
