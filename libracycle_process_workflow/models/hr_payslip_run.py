from urllib.parse import urlencode, urljoin

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HrPayslipRun(models.Model):

    _name = "hr.payslip.run"
    _inherit = ["hr.payslip.run", "mail.thread"]

    state = fields.Selection(
        selection_add=[
            ("admin", "Await Admin"),
            ("officer", "Await Officer"),
            ("qac", "Await QAC"),
            ("director_1", "Await Director I"),
            ("director_2", "Await Director II"),
            ("account", "Await Account"),
            ("close",),
        ],
        ondelete={
            "admin": lambda m: m.write({"state": "draft"}),
            "officer": lambda m: m.write({"state": "draft"}),
            "qac": lambda m: m.write({"state": "draft"}),
            "director_1": lambda m: m.write({"state": "draft"}),
            "director_2": lambda m: m.write({"state": "draft"}),
        },
        tracking=True,
    )

    def action_submit_to_admin(self):
        for rec in self:

            url = self.request_link()
            email_from = self.env.user.partner_id.email
            recipients = users = "".join(
                self.env.ref("libracycle_process_workflow.group_officer").users.mapped(
                    "email"
                )
            )
            mail_template = self.env.ref(
                "libracycle_process_workflow.mail_template_payslip_run"
            )
            mail_template.with_context(
                {
                    "recipient": recipients,
                    "url": url,
                    "email_from": email_from,
                    "title": "Officer",
                }
            ).send_mail(self.id, force_send=False)
            rec.write({"state": "admin"})

    def action_submit_to_officer(self):
        for rec in self:
            url = self.request_link()
            email_from = self.env.user.partner_id.email
            recipients = users = "".join(
                self.env.ref("libracycle_process_workflow.group_qac").users.mapped(
                    "email"
                )
            )
            mail_template = self.env.ref(
                "libracycle_process_workflow.mail_template_payslip_run"
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

    def action_submit_to_qac(self):
        for rec in self:
            url = self.request_link()
            email_from = self.env.user.partner_id.email
            recipients = users = "".join(
                self.env.ref("libracycle_process_workflow.group_qac").users.mapped(
                    "email"
                )
            )
            mail_template = self.env.ref(
                "libracycle_process_workflow.mail_template_payslip_run"
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
                "libracycle_process_workflow.mail_template_payslip_run"
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
                "libracycle_process_workflow.mail_template_payslip_run"
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
            url = self.request_link()
            email_from = self.env.user.partner_id.email
            recipients = users = "".join(
                self.env.ref(
                    "libracycle_process_workflow.group_director_2"
                ).users.mapped("email")
            )
            mail_template = self.env.ref(
                "libracycle_process_workflow.mail_template_payslip_run"
            )
            mail_template.with_context(
                {
                    "recipient": recipients,
                    "url": url,
                    "email_from": email_from,
                    "title": "Officer",
                }
            ).send_mail(self.id, force_send=False)
            rec.write({"state": "account"})

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