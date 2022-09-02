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
            recipients = users = "".join(
                self.env.ref("account.group_account_manager").users.mapped(
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
            rec.write({'state': 'review'})

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



class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def write(self, vals):
        # OVERRIDE
        ACCOUNTING_FIELDS = ('debit', 'credit', 'amount_currency')
        BUSINESS_FIELDS = ('price_unit', 'quantity', 'discount', 'tax_ids')
        PROTECTED_FIELDS_TAX_LOCK_DATE = ['debit', 'credit', 'tax_line_id', 'tax_ids', 'tax_tag_ids']
        PROTECTED_FIELDS_LOCK_DATE = PROTECTED_FIELDS_TAX_LOCK_DATE + ['account_id', 'journal_id', 'amount_currency', 'currency_id', 'partner_id']
        PROTECTED_FIELDS_RECONCILIATION = ('account_id', 'date', 'debit', 'credit', 'amount_currency', 'currency_id')

        account_to_write = self.env['account.account'].browse(vals['account_id']) if 'account_id' in vals else None

        # Check writing a deprecated account.
        if account_to_write and account_to_write.deprecated:
            raise UserError(_('You cannot use a deprecated account.'))

        for line in self:
            if line.parent_state == 'posted':
                if line.move_id.restrict_mode_hash_table and set(vals).intersection(INTEGRITY_HASH_LINE_FIELDS):
                    raise UserError(_("You cannot edit the following fields due to restrict mode being activated on the journal: %s.") % ', '.join(INTEGRITY_HASH_LINE_FIELDS))
                if any(key in vals for key in ('tax_ids', 'tax_line_id')):
                    raise UserError(_('You cannot modify the taxes related to a posted journal item, you should reset the journal entry to draft to do so.'))

            # Check the lock date.
            if line.parent_state == 'posted' and any(self.env['account.move']._field_will_change(line, vals, field_name) for field_name in PROTECTED_FIELDS_LOCK_DATE):
                line.move_id._check_fiscalyear_lock_date()

            # Check the tax lock date.
            if line.parent_state == 'posted' and any(self.env['account.move']._field_will_change(line, vals, field_name) for field_name in PROTECTED_FIELDS_TAX_LOCK_DATE):
                line._check_tax_lock_date()

            # Check the reconciliation.
            if any(self.env['account.move']._field_will_change(line, vals, field_name) for field_name in PROTECTED_FIELDS_RECONCILIATION):
                line._check_reconciliation()

            # Check switching receivable / payable accounts.
            if account_to_write:
                account_type = line.account_id.user_type_id.type
                if line.move_id.is_sale_document(include_receipts=True):
                    if (account_type == 'receivable' and account_to_write.user_type_id.type != account_type) \
                            or (account_type != 'receivable' and account_to_write.user_type_id.type == 'receivable'):
                        raise UserError(_("You can only set an account having the receivable type on payment terms lines for customer invoice."))
                if line.move_id.is_purchase_document(include_receipts=True):
                    if (account_type == 'payable' and account_to_write.user_type_id.type != account_type) \
                            or (account_type != 'payable' and account_to_write.user_type_id.type == 'payable'):
                        # raise UserError(_("You can only set an account having the payable type on payment terms lines for vendor bill."))
                        pass

        # Tracking stuff can be skipped for perfs using tracking_disable context key
        if not self.env.context.get('tracking_disable', False):
            # Get all tracked fields (without related fields because these fields must be manage on their own model)
            tracking_fields = []
            for value in vals:
                field = self._fields[value]
                if hasattr(field, 'related') and field.related:
                    continue # We don't want to track related field.
                if hasattr(field, 'tracking') and field.tracking:
                    tracking_fields.append(value)
            ref_fields = self.env['account.move.line'].fields_get(tracking_fields)

            # Get initial values for each line
            move_initial_values = {}
            for line in self.filtered(lambda l: l.move_id.posted_before): # Only lines with posted once move.
                for field in tracking_fields:
                    # Group initial values by move_id
                    if line.move_id.id not in move_initial_values:
                        move_initial_values[line.move_id.id] = {}
                    move_initial_values[line.move_id.id].update({field: line[field]})

        result = True
        for line in self:
            cleaned_vals = line.move_id._cleanup_write_orm_values(line, vals)
            if not cleaned_vals:
                continue

            # Auto-fill amount_currency if working in single-currency.
            if 'currency_id' not in cleaned_vals \
                and line.currency_id == line.company_currency_id \
                and any(field_name in cleaned_vals for field_name in ('debit', 'credit')):
                cleaned_vals.update({
                    'amount_currency': vals.get('debit', 0.0) - vals.get('credit', 0.0),
                })

            result |= super(AccountMoveLine, line).write(cleaned_vals)

            if not line.move_id.is_invoice(include_receipts=True):
                continue

            # Ensure consistency between accounting & business fields.
            # As we can't express such synchronization as computed fields without cycling, we need to do it both
            # in onchange and in create/write. So, if something changed in accounting [resp. business] fields,
            # business [resp. accounting] fields are recomputed.
            if any(field in cleaned_vals for field in ACCOUNTING_FIELDS):
                price_subtotal = line._get_price_total_and_subtotal().get('price_subtotal', 0.0)
                to_write = line._get_fields_onchange_balance(price_subtotal=price_subtotal)
                to_write.update(line._get_price_total_and_subtotal(
                    price_unit=to_write.get('price_unit', line.price_unit),
                    quantity=to_write.get('quantity', line.quantity),
                    discount=to_write.get('discount', line.discount),
                ))
                result |= super(AccountMoveLine, line).write(to_write)
            elif any(field in cleaned_vals for field in BUSINESS_FIELDS):
                to_write = line._get_price_total_and_subtotal()
                to_write.update(line._get_fields_onchange_subtotal(
                    price_subtotal=to_write['price_subtotal'],
                ))
                result |= super(AccountMoveLine, line).write(to_write)

        # Check total_debit == total_credit in the related moves.
        if self._context.get('check_move_validity', True):
            self.mapped('move_id')._check_balanced()

        self.mapped('move_id')._synchronize_business_models({'line_ids'})

        if not self.env.context.get('tracking_disable', False):
            # Log changes to move lines on each move
            for move_id, modified_lines in move_initial_values.items():
                for line in self.filtered(lambda l: l.move_id.id == move_id):
                    tracking_value_ids = line._mail_track(ref_fields, modified_lines)[1]
                    if tracking_value_ids:
                        msg = f"{html_escape(_('Journal Item'))} <a href=# data-oe-model=account.move.line data-oe-id={line.id}>#{line.id}</a> {html_escape(_('updated'))}"
                        line.move_id._message_log(
                            body=msg,
                            tracking_value_ids=tracking_value_ids
                        )

        return result
