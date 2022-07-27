from odoo import models, fields, api
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
                subject = "Approval Request for %s" % (self.name,)
                body = """<p>%s</p>
                <p>%s has been submitted for your attention, kindy check and attend to the document accordingly.</p>
                <br/>
                <p>Regards</p>
            """ % (self.env.user.name, self.name)
                self.send_notification(body, subject, group="libracycle_process_workflow.group_officer")
                rec.write({"state": "officer"})
            else:
                raise ValidationError("Add a partner to the bill")


    def action_officer_approve(self):
        for rec in self:
            subject = "Approval Request for %s" % (self.name,)
            body = """<p>%s</p>
                <p>%s has been submitted for your attention, kindy check and attend to the document accordingly.</p>
                <br/>
                <p>Regards</p>
            """ % (self.env.user.name, self.name)
            self.send_notification(body, subject, group="libracycle_process_workflow.group_qac")
            rec.write({'state': 'qac'})

    def action_qac_approve(self):
        for rec in self:
            subject = "Approval Request for %s" % (self.name,)
            body = """<p>%s</p>
                <p>%s has been submitted for your attention, kindy check and attend to the document accordingly.</p>
                <br/>
                <p>Regards</p>
            """ % (self.env.user.name, self.name)
            self.send_notification(body, subject, group="libracycle_process_workflow.group_director_1")
            rec.write({'state': 'director_1'})

    def action_director1_approve(self):
        for rec in self:
            subject = "Approval Request for %s" % (self.name,)
            body = """<p>%s</p>
                <p>%s has been submitted for your attention, kindy check and attend to the document accordingly.</p>
                <br/>
                <p>Regards</p>
            """ % (self.env.user.name, self.name)
            self.send_notification(body, subject, group="libracycle_process_workflow.group_director_2")
            rec.write({'state': 'director_2'})

    def action_director2_approve(self):
        for rec in self:
            rec.action_post()


    def action_reject(self):
        pass

    def send_notification(self, body, subject, group):
        partner_ids = []
        
        users = self.env.ref(group).users
        for user in users:
            partner_ids.append(user.partner_id.id)

        if partner_ids:
            self.message_post(
                body=body,
                subject=subject,
                partner_ids=partner_ids,
                message_type="email",
            )
        return True
