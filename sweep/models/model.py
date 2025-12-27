from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
import logging
from datetime import datetime

_logger = logging.getLogger(__name__)


class ProductTempExt(models.Model):
    _inherit = 'product.template'

    is_sweep_product = fields.Boolean(string="Is a Sweep Product")
    sweep_account_id = fields.Many2one('account.account')


class ResCompanyExt(models.Model):
    _inherit = 'res.company'

    sweep_start_date = fields.Date('Start Date')
    sweep_end_date = fields.Date('End Date')


class AccountMoveExt(models.Model):
    _inherit = 'account.move'

    is_a_sweep_je = fields.Boolean()
    ref_line_id = fields.Many2one('account.move.line', "Reference Line")
    # analytic_account_id = fields.Many2one(string='Project')

    # vendor_bill_line_id = fields.Many2one('account.move.line', "Vendor Bill Line")

    # def button_cancel(self):
    #     logging.info("Hamza Ilyas ----> button_cancel Called")
    #     for move in self:
    #         if not move.journal_id.update_posted:
    #             raise UserError(
    #                 _('You cannot modify a posted entry of this journal.\nFirst you should set the journal to allow cancelling entries.'))
    #         else:
    #             if move.is_a_sweep_je:
    #                 if move.ref:
    #                     bill = self.env['account.move'].search([('number', '=', move.ref)])
    #                     if bill:
    #                         self.unswept_bill_lines(move)
    #                     else:
    #                         # receipt = self.env['account.voucher'].search([('number', '=', move.ref)])
    #                         # if receipt:
    #                         #     self.unswept_voucher_lines(move)
    #                         # else:
    #                             expense = self.env['hr.expense'].search([('name', '=', move.ref)])
    #                             if expense:
    #                                 self.unswept_expense(expense)
    #                 # for line in move.line_ids:
    #                 #     line.swept = False
    #
    #     if self.ids:
    #         self.check_access_rights('write')
    #         self.check_access_rule('write')
    #         self._check_lock_date()
    #         self._cr.execute('UPDATE account_move ' \
    #                          'SET state=%s ' \
    #                          'WHERE id IN %s', ('draft', tuple(self.ids),))
    #         self.invalidate_cache()
    #     self._check_lock_date()
    #
    #     # on cancelling of sweep journal entry it will be removed
    #     if self.is_a_sweep_je:
    #         logging.info("Hamza Ilyas ----> unlinking swept journal entry")
    #         self.unlink()
    #     return True

    def button_cancel(self):
        logging.info("Hamza Ilyas ----> button_cancel Called")
        self.write({'auto_post': False, 'state': 'cancel'})
        if self.is_a_sweep_je:
            if self.ref:
                if self.ref_line_id:
                    self.unswept_move_lines()
                else:
                    expense = self.env['hr.expense'].search([('name', '=', self.ref)])
                    if expense:
                        self.unswept_expense(expense)
            action = self.env.ref('account.action_move_journal_line').read()[0]
            self.unlink()
            return action

    def unswept_move_lines(self):
        line = self.ref_line_id
        if line:
            line.swept = False
            line.invoice_line_id.swept = False

    
    def unswept_expense(self, expense):
        expense.swept = False
        if expense.invoice_line_id:
            expense.invoice_line_id.swept = False

    def cron_sweep_entries(self):
        start_date = self.env.company.sweep_start_date
        end_date = self.env.company.sweep_end_date
        invoices = self.env['account.move'].search([('move_type', '=', 'out_invoice'), ('state', '=', 'posted'), '&',
                                                    ('invoice_date', '>=', start_date),
                                                    ('invoice_date', '<=', end_date)])
        for invoice in invoices.filtered(lambda inv: inv.invoice_line_ids is not False):
            for invoice_line in invoice.invoice_line_ids.filtered(lambda line: line.swept is False):
                expenses = self.check_ili_in_expenses(invoice_line, start_date, end_date)
                for exp in expenses:
                    self.swept_journal_entry(exp, end_date)
                    invoice_line.swept = True

                purchase_receipt_lines = self.check_ili_in_purchase_receipts(invoice_line, start_date, end_date)
                for prl in purchase_receipt_lines:
                    self.swept_journal_entry(prl, end_date)
                    invoice_line.swept = True


                sale_receipt_lines = self.check_ili_in_sale_receipts(invoice_line, start_date, end_date)
                for srl in sale_receipt_lines:
                    self.swept_journal_entry(srl, end_date)
                    invoice_line.swept = True
                bill_lines = self.check_ili_in_vendor_bills(invoice_line, start_date, end_date)
                for bl in bill_lines:
                    self.swept_journal_entry(bl, end_date)
                    invoice_line.swept = True

    def swept_journal_entry(self, record, end_date):
        journal = self.env['sweep.journal'].search([])
        sweep_journal = False
        if journal:
            sweep_journal = journal.journal_id
        else:
            raise ValidationError("Sweep Journal is not set")
        if record._name == 'hr.expense':
            self.create_swept_journal_entry(record.name, False, sweep_journal, record.total_amount, record.product_id,
                                            record.analytic_account_id, record.partner_id, end_date)
        elif record._name == 'account.move.line':
            self.create_swept_journal_entry(record.move_id.name, record, sweep_journal, record.price_subtotal,
                                            record.product_id, record.analytic_account_id, record.partner_id, end_date)
    def create_swept_journal_entry(self, je_ref, ref_line_id, je_journal, ji_amount, ji_product, analytic_account_id, partner, end_date):
        a_a_project = self.env['account.analytic.account'].search([('id', '=', analytic_account_id.id)])
        if a_a_project:
            analytic_account_id = a_a_project.id
        else:
            analytic_account_id = False
        self.env.cr.commit()
        if ji_product.property_account_expense_id:
            move = self.env['account.move'].create({'ref': je_ref, 'journal_id': je_journal.id, 'state': 'draft',
                                                    'is_a_sweep_je': True, 'ref_line_id': ref_line_id, 'date': end_date,
                                                    })

            self.env.cr.execute("UPDATE ACCOUNT_MOVE SET DATE = '%s' WHERE id=%s" % (end_date, move.id))

            if move.ref_line_id:
                if move.ref_line_id.move_id.move_type == 'out_receipt':
                    move.write({'line_ids': [
                        (0, 0, {'account_id': ji_product.property_account_expense_id.id,
                                'name': ji_product.name,
                                'partner_id': partner.id,
                                'debit': 0.0,
                                'credit': ji_amount,
                                'move_id': move.id,
                                'project_id_hi': analytic_account_id,
                                'swept': True,
                                }),
                        (0, 0, {'account_id': ji_product.sweep_account_id.id,
                                'name': ji_product.name,
                                'partner_id': partner.id,
                                'debit': ji_amount,
                                'credit': 0.0,
                                'move_id': move.id,
                                'project_id_hi': analytic_account_id,
                                'swept': True,
                                }),
                    ], })
                else:
                    move.write({'line_ids': [
                        (0, 0, {'account_id': ji_product.property_account_expense_id.id,
                                'name': ji_product.name,
                                'partner_id': partner.id,
                                'debit': ji_amount,
                                'credit': 0.0,
                                'move_id': move.id,
                                'project_id_hi': analytic_account_id,
                                'swept': True,
                                }),
                        (0, 0, {'account_id': ji_product.sweep_account_id.id,
                                'name': ji_product.name,
                                'partner_id': partner.id,
                                'debit': 0.0,
                                'credit': ji_amount,
                                'move_id': move.id,
                                'project_id_hi': analytic_account_id,
                                'swept': True,
                                }),
                    ], })
            else:
                move.write({'line_ids': [
                    (0, 0, {'account_id': ji_product.property_account_expense_id.id,
                            'name': ji_product.name,
                            'partner_id': partner.id,
                            'debit': ji_amount,
                            'credit': 0.0,
                            'move_id': move.id,
                            'project_id_hi': analytic_account_id,
                            'swept': True,
                            }),
                    (0, 0, {'account_id': ji_product.sweep_account_id.id,
                            'name': ji_product.name,
                            'partner_id': partner.id,
                            'debit': 0.0,
                            'credit': ji_amount,
                            'move_id': move.id,
                            'project_id_hi': analytic_account_id,
                            'swept': True,
                            }),
                ], })
            if move:
                move.action_post()
                logging.info("Hamza Ilyas ----> Swept Journal Entry Created & posted Successfully")

    def check_ili_in_expenses(self, invoice_line, start_date, end_date):
        logging.info("Hamza Ilyas ----> check_ili_in_expenses Called")
        expenses = self.env['hr.expense'].search([('state', 'in', ('done', 'approved')), '&',
                                                  ('date', '>=', start_date), ('date', '<=', end_date)])
        exp_rt = []
        for expense in expenses:
            # if expense.product_id == invoice_line.product_id and \
            #         expense.analytic_account_id == invoice_line.analytic_account_id and not expense.swept:
            # if expense.product_id == invoice_line.product_id and not expense.swept:
            if (expense.product_id == invoice_line.product_id and
                    expense.analytic_account_id == invoice_line.analytic_account_id and not expense.swept):
                expense.swept = True
                expense.invoice_line_id = invoice_line
                exp_rt.append(expense)
            # else:
            #     continue

        return exp_rt

    def check_ili_in_purchase_receipts(self, invoice_line, start_date, end_date):
        purchase_receipts = self.env['account.move'].search(
            [('state', '=', 'posted'), ('move_type', '=', 'in_receipt'), '&',
             ('invoice_date', '>=', start_date), ('invoice_date', '<=', end_date)])
        rec_rt = []
        for receipt in purchase_receipts:
            for receipt_line in receipt.invoice_line_ids:
                if (receipt_line.product_id == invoice_line.product_id and
                        receipt_line.analytic_account_id == invoice_line.analytic_account_id and not
                        receipt_line.swept):
                    receipt_line.swept = True
                    receipt_line.invoice_line_id = invoice_line.id
                    rec_rt.append(receipt_line)
        return rec_rt

    def check_ili_in_sale_receipts(self, invoice_line, start_date, end_date):
        sale_receipts = self.env['account.move'].search([('state', '=', 'posted'), ('move_type', '=', 'out_receipt'),
                                                         '&', ('invoice_date', '>=', start_date),
                                                         ('invoice_date', '<=', end_date)])
        recs_rt = []
        for receipt in sale_receipts:
            for receipt_line in receipt.invoice_line_ids:
                if (receipt_line.product_id == invoice_line.product_id and
                        receipt_line.analytic_account_id == invoice_line.analytic_account_id and not
                        receipt_line.swept):
                    receipt_line.swept = True
                    receipt_line.invoice_line_id = invoice_line.id
                    recs_rt.append(receipt_line)
        return recs_rt

    def check_ili_in_vendor_bills(self, invoice_line, start_date, end_date):
        vendor_bills = self.env['account.move'].search([('state', '=', 'posted'), ('move_type', '=', 'in_invoice'),
                                                        '&', ('invoice_date', '>=', start_date),
                                                        ('invoice_date', '<=', end_date)])
        ven_rt = []
        for bill in vendor_bills:
            for bill_line in bill.invoice_line_ids:
                if (bill_line.product_id == invoice_line.product_id and
                        bill_line.analytic_account_id == invoice_line.analytic_account_id and not bill_line.swept):
                    bill_line.swept = True
                    bill_line.invoice_line_id = invoice_line.id
                    ven_rt.append(bill_line)
        return ven_rt


class AccountMoveLineExt(models.Model):
    _inherit = 'account.move.line'

    swept = fields.Boolean(string="Swept", readonly=True)

    invoice_line_id = fields.Many2one("account.move.line", "Invoice Line")

    project_id_hi = fields.Many2one('account.analytic.account', string='Project')

    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.move_id.move_type in ['in_invoice', 'in_receipt', 'out_receipt']:
            if self.product_id:
                if self.product_id.is_sweep_product:
                    self.account_id = self.product_id.sweep_account_id


class HrExpenseExt(models.Model):
    _inherit = 'hr.expense'

    # product_id = fields.Many2one("product.product", "Product")

    swept = fields.Boolean(string="Swept", readonly=True)
    invoice_line_id = fields.Many2one("account.move.line", "Invoice Line")

    @api.onchange('product_id')
    def onchange_product_id(self):
        logging.info("Hamza Ilyas ----> onchange_product_id Called on hr.expense")
        if self.product_id:
            if self.product_id.is_sweep_product:
                self.account_id = self.product_id.sweep_account_id


# class AccountVoucherExt(models.Model):
#     _inherit = 'account.voucher.line'
#
#     swept = fields.Boolean(string="Swept", readonly=True)
#     invoice_line_id = fields.Many2one("account.move.line", "Invoice Line")
#
#
#     # @api.model
#     # def create(self, vals):
#     #     if 'product_id' in vals:
#     #         if vals['product_id']:
#     #             product = self.env['product.product'].search([('id', '=', vals['product_id'])])
#     #             if product:
#     #                 if product.is_sweep_product and product.sweep_account_id:
#     #                     vals['account_id'] = product.sweep_account_id.id
#     #
#     #     rec = super(AccountVoucherExt, self).create(vals)
#     #     return rec
#
#     #@api.multi
#     # def write(self, vals):
#     #     return super(AccountVoucherExt, self).write(vals)
#
#     @api.onchange('product_id')
#     def onchange_product_id(self):
#         logging.info("Hamza Ilyas ----> onchange_product_id Called on account voucher line")
#         if self.product_id:
#             temp = self.product_id
#             self.product_id = self.env['product.product'].search([])[1]
#             self.product_id = temp
#             if self.product_id.is_sweep_product:
#                 logging.info("Hamza Ilyas ----> is_sweep_product")
#                 self.account_id = self.product_id.sweep_account_id.id
#                 self.write({
#                     'account_id': self.product_id.sweep_account_id.id
#                 })
#                 self.account_id = self.product_id.sweep_account_id.id
#                 logging.info("Hamza Ilyas ----> account_id set as :")
#                 logging.info(self.account_id.name)
#                 # self.check_account_id(self.product_id, self.account_id)
#
#     def check_account_id(self, product_id, account_id):
#         logging.info("Hamza Ilyas ----> check_account_id Called")
#         if product_id.is_sweep_product and product_id.sweep_account_id:
#             logging.info("11")
#             if product_id.sweep_account_id.id != account_id.id:
#                 logging.info("22")
#                 self.onchange_product_id()
#                 logging.info("Hamza Ilyas ----> finish check_account_id")


class SweepJournal(models.Model):
    _name = 'sweep.journal'

    journal_id = fields.Many2one('account.journal', string='Journal')

# class AccountMoveLineExt(models.Model):
#     _inherit = 'account.move.line'
#
#     swept = fields.Boolean(string="Swept", readonly=True)


# class AccountMoveExt(models.Model):
#     _inherit = 'account.move'
#
#     is_a_sweep_je = fields.Boolean()
#     voucher_line_id = fields.Many2one('account.voucher.line', "Voucher Line")
#     vendor_bill_line_id = fields.Many2one('account.move.line', "Vendor Bill Line")
#
#     def button_cancel(self):
#         logging.info("Hamza Ilyas ----> button_cancel Called")
#         for move in self:
#             if not move.journal_id.update_posted:
#                 raise UserError(
#                     _('You cannot modify a posted entry of this journal.\nFirst you should set the journal to allow cancelling entries.'))
#             else:
#                 if move.is_a_sweep_je:
#                     if move.ref:
#                         bill = self.env['account.move'].search([('number', '=', move.ref)])
#                         if bill:
#                             self.unswept_bill_lines(move)
#                         else:
#                             receipt = self.env['account.voucher'].search([('number', '=', move.ref)])
#                             if receipt:
#                                 self.unswept_voucher_lines(move)
#                             else:
#                                 expense = self.env['hr.expense'].search([('name', '=', move.ref)])
#                                 if expense:
#                                     self.unswept_expense(expense)
#                     # for line in move.line_ids:
#                     #     line.swept = False
#
#         if self.ids:
#             self.check_access_rights('write')
#             self.check_access_rule('write')
#             self._check_lock_date()
#             self._cr.execute('UPDATE account_move ' \
#                              'SET state=%s ' \
#                              'WHERE id IN %s', ('draft', tuple(self.ids),))
#             self.invalidate_cache()
#         self._check_lock_date()
#
#         # on cancelling of sweep journal entry it will be removed
#         if self.is_a_sweep_je:
#             logging.info("Hamza Ilyas ----> unlinking swept journal entry")
#             self.unlink()
#         return True
#
#     def unswept_bill_lines(self, move):
#         # for line in bill.invoice_line_ids:
#         #     for move_line in move.line_ids:
#         #         if move_line.product_id.name == line.name and move_line.analytical_account_id == line.account_analytic_id:
#         line = move.vendor_bill_line_id
#         line.swept = False
#         line.invoice_line_id.swept = False
#         line.invoice_id.swept = False
#
#     def unswept_voucher_lines(self, move):
#         # for line in recipt.line_ids:
#         #     for move_line in move.line_ids:
#         #         if move_line.name == line.name and move_line.analytical_account_id == line.account_analytic_id:
#         line = move.voucher_line_id
#         line.swept = False
#         line.invoice_line_id.swept = False
#         line.voucher_id.swept = False
#
#     def unswept_expense(self, expense):
#         expense.swept = False
#         expense.invoice_line_id.swept = False
