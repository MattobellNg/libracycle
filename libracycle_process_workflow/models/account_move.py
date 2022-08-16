from urllib.parse import urlencode, urljoin

from odoo import api, fields, models
from odoo.exceptions import ValidationError

class AccountMove(models.Model):
    _inherit = "account.move"

    state = fields.Selection(
        selection_add=[
            ("posted",),
            ("admin", "Admin"),
            ("officer", "Officer"),
            ("qac", "QAC"),
            ("director_1", "Director 1"),
            ("director_2", "Director 2"),
        ],
        ondelete={
            "admin": lambda m: m.write({"state": "draft"}),
            "officer": lambda m: m.write({"state": "draft"}),
            "qac": lambda m: m.write({"state": "draft"}),
            "director_1": lambda m: m.write({"state": "draft"}),
            "director_2": lambda m: m.write({"state": "draft"}),
        },
    )

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
                    "libracycle_process_workflow.libracycle_mail_template"
                )
                mail_template.with_context(
                    {
                        "recipient": recipients,
                        "url": url,
                        "email_from": email_from,
                        "title": "Officer",
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
                "libracycle_process_workflow.libracycle_mail_template"
            )
            mail_template.with_context(
                {
                    "recipient": recipients,
                    "url": url,
                    "email_from": email_from,
                    "title": "Officer",
                }
            ).send_mail(self.id, force_send=False)
            rec.write({"state": "qac"})

    def action_qac_approve(self):
        for rec in self:
            url = self.request_link()
            email_from = self.env.user.partner_id.email
            recipients = users = "".join(
                self.env.ref(
                    "libracycle_process_workflow.group_director_1"
                ).users.mapped("email")
            )
            mail_template = self.env.ref(
                "libracycle_process_workflow.libracycle_mail_template"
            )
            mail_template.with_context(
                {
                    "recipient": recipients,
                    "url": url,
                    "email_from": email_from,
                    "title": "Officer",
                }
            ).send_mail(self.id, force_send=False)
            rec.write({"state": "director_1"})

    def action_director1_approve(self):
        for rec in self:
            url = self.request_link()
            email_from = self.env.user.partner_id.email
            recipients = users = "".join(
                self.env.ref(
                    "libracycle_process_workflow.group_director_2"
                ).users.mapped("email")
            )
            mail_template = self.env.ref(
                "libracycle_process_workflow.libracycle_mail_template"
            )
            mail_template.with_context(
                {
                    "recipient": recipients,
                    "url": url,
                    "email_from": email_from,
                    "title": "Officer",
                }
            ).send_mail(self.id, force_send=False)
            rec.write({"state": "director_2"})

    def action_director2_approve(self):
        for rec in self:
            rec.action_post()

    def action_reject(self):
        pass

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
