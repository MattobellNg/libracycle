from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import ValidationError
import json
import logging

_logger = logging.getLogger(__name__)


class Project(models.Model):
    _inherit = "project.project"

    wht = fields.Float("With Holding Tax")

    # Total Invoice Value(N) minus Total Cost.

    total_cost = fields.Float(string="Total Cost", compute="compute_total_cost")
    total_income = fields.Float(string="Total Income", compute="compute_total_income")

    total_profit = fields.Float(string="Total Profit")

    # This all fields below is for vendor bill/expense

    project_product_duty = fields.Integer(string="Project Duty", compute="compute_project_product_duty")
    project_shipping_charge = fields.Integer(string="Project Shipping Charge", compute="compute_project_shipping_charge")
    project_terminal_charge = fields.Float(string="Project Terminal Charge", compute="compute_project_terminal_charge")
    project_nafdac = fields.Integer(string="Project Nafdac", compute="compute_project_nafdac")
    project_son = fields.Integer(string="Project SON", compute="compute_project_son")
    project_agency = fields.Integer(string="Project Agency", compute="compute_project_agency")
    project_transportation = fields.Integer(string="Project Transportation", compute="compute_project_transportation")
    project_others = fields.Integer(string="Project Others", compute="compute_project_others")

    # This all fieds below is for customer invoice/income

    customer_duty = fields.Integer(string="Duty Income", compute="compute_customer_duty")
    customer_shipping_charge = fields.Integer(string="Customer Shipping Charge",
                                              compute="compute_customer_shipping_charge")
    customer_terminal_charge = fields.Integer(string="Customer Terminal Charge",
                                              compute="compute_customer_terminal_charge")
    customer_nafdac = fields.Integer(string="Customer Nafdac", compute="compute_customer_nafdac")
    customer_son = fields.Integer(string="Customer SON", compute="compute_customer_son")
    customer_agency = fields.Integer(string="Customer Agency", compute="compute_customer_agency")
    customer_transportation = fields.Integer(string="Customer Transportation",
                                             compute="compute_customer_transportation")
    customer_others = fields.Integer(string="Customer Others", compute="compute_customer_others")

    customer_untaxed_value = fields.Integer(string="Invoice Value(N)", compute="compute_customer_invoice_values")
    customer_vat = fields.Integer(string="VAT(N)", compute="compute_customer_invoice_values")
    customer_total_invoice_value = fields.Integer(string="Total Invoice Value(N)",
                                                  compute="compute_customer_invoice_values")
    customer_invoice_paid = fields.Integer(string="Paid", compute="compute_customer_invoice_values")
    customer_invoice_unpaid = fields.Integer(string="Not Paid", compute="compute_customer_invoice_values")

    # For Smart Buttons

    duty_count = fields.Integer(string="Duty Invoice Line", compute='compute_duty_count')
    duty_move_line_ids = fields.One2many("account.move.line", "project_id", string="Duty Move Lines",
                                         compute="compute_duty_count")
    shipping_count = fields.Integer(string="Shipping Invoice Line", compute='compute_shipping_count')
    shipping_move_line_ids = fields.One2many("account.move.line", "project_id", string="Shipping Move Lines",
                                             compute="compute_shipping_count")
    terminal_count = fields.Integer(string="Terminal Invoice Line", compute='compute_terminal_count')
    terminal_move_line_ids = fields.One2many("account.move.line", "project_id", string="Terminal Move Lines",
                                             compute="compute_terminal_count")
    nafdac_count = fields.Integer(string="Nafdac Invoice Line", compute='compute_nafdac_count')
    nafdac_move_line_ids = fields.One2many("account.move.line", "project_id", string="NAFDAC Move Lines",
                                           compute="compute_nafdac_count")
    son_count = fields.Integer(string="Son Invoice Line", compute='compute_son_count')
    son_move_line_ids = fields.One2many("account.move.line", "project_id", string="SON Move Lines",
                                        compute="compute_son_count")
    agency_count = fields.Integer(string="Agency Invoice Line", compute='compute_agency_count')
    agency_move_line_ids = fields.One2many("account.move.line", "project_id", string="Agency Move Lines",
                                           compute="compute_agency_count")
    transportation_count = fields.Integer(string="Transportation Invoice Line", compute='compute_transportation_count')
    transportation_move_line_ids = fields.One2many("account.move.line", "project_id",
                                                   string="Transportation Move Lines",
                                                   compute="compute_transportation_count")
    others_count = fields.Integer(string="Others Invoice Line", compute='compute_others_count')
    others_move_line_ids = fields.One2many("account.move.line", "project_id", string="Others Move Lines",
                                           compute="compute_others_count")

    move_line = fields.Char(string="Transportation Move Line")
    job_type = fields.Char(string="Job Type", related='type_id.name')

    def compute_total_income(self):
        for rec in self:
            rec.total_income = rec.customer_duty + rec.customer_shipping_charge + rec.customer_terminal_charge + \
                               rec.customer_nafdac + rec.customer_son + rec.customer_agency + rec.customer_transportation + \
                               rec.customer_others

    def compute_total_cost(self):
        for rec in self:
            rec.total_cost = rec.project_product_duty + rec.project_shipping_charge + rec.project_terminal_charge + \
                             rec.project_nafdac + rec.project_son + rec.project_agency + rec.project_transportation + \
                             rec.project_others

    def compute_customer_duty(self):
        print("compute_customer_duty called XXXXXXXXXXXX")
        for rec in self:
            move_lines = rec.env['account.move.line'].search([
                ('move_id.move_type', '=', 'out_invoice'),
                ('analytic_account_id', '=', rec.analytic_account_id.id),
                ('product_id.product_duty', '=', True)])
            customer_duty = 0
            for line in move_lines:
                customer_duty += line.price_subtotal
            rec.customer_duty = customer_duty

    def compute_customer_shipping_charge(self):
        print("compute_customer_shipping_charge called XXXXXXXXXXXX")
        for rec in self:
            move_lines = rec.env['account.move.line'].search([
                ('move_id.move_type', '=', 'out_invoice'),
                ('analytic_account_id', '=', rec.analytic_account_id.id),
                ('product_id.shipping_charge', '=', True)])
            customer_shipping = 0
            for line in move_lines:
                customer_shipping += line.price_subtotal
            rec.customer_shipping_charge = customer_shipping

    def compute_customer_terminal_charge(self):
        print("compute_customer_terminal_charge called XXXXXXXXXXXX")
        for rec in self:
            move_lines = rec.env['account.move.line'].search([
                ('move_id.move_type', '=', 'out_invoice'),
                ('analytic_account_id', '=', rec.analytic_account_id.id),
                ('product_id.terminal_charge', '=', True)])
            terminal_charge = 0
            for line in move_lines:
                terminal_charge += line.price_subtotal
            rec.customer_terminal_charge = terminal_charge

    def compute_customer_nafdac(self):
        print("compute_customer_nafdac called XXXXXXXXXXXX")
        for rec in self:
            move_lines = rec.env['account.move.line'].search([
                ('move_id.move_type', '=', 'out_invoice'),
                ('analytic_account_id', '=', rec.analytic_account_id.id),
                ('product_id.nafdac', '=', True)])
            customer_nafdac = 0
            for line in move_lines:
                customer_nafdac += line.price_subtotal
            rec.customer_nafdac = customer_nafdac

    def compute_customer_son(self):
        print("compute_customer_son called XXXXXXXXXXXX")
        for rec in self:
            move_lines = rec.env['account.move.line'].search([
                ('move_id.move_type', '=', 'out_invoice'),
                ('analytic_account_id', '=', rec.analytic_account_id.id),
                ('product_id.son', '=', True)])
            customer_son = 0
            for line in move_lines:
                customer_son += line.price_subtotal
            rec.customer_son = customer_son

    def compute_customer_agency(self):
        print("compute_customer_agency called XXXXXXXXXXXX")
        for rec in self:
            move_lines = rec.env['account.move.line'].search([
                ('move_id.move_type', '=', 'out_invoice'),
                ('analytic_account_id', '=', rec.analytic_account_id.id),
                ('product_id.agency', '=', True)])
            customer_agency = 0
            for line in move_lines:
                customer_agency += line.price_subtotal
            rec.customer_agency = customer_agency

    def compute_customer_transportation(self):
        print("compute_customer_transportation called XXXXXXXXXXXX")
        for rec in self:
            move_lines = rec.env['account.move.line'].search([
                ('move_id.move_type', '=', 'out_invoice'),
                ('analytic_account_id', '=', rec.analytic_account_id.id),
                ('product_id.transportation', '=', True)])
            customer_transportation = 0
            for line in move_lines:
                customer_transportation += line.price_subtotal
            rec.customer_transportation = customer_transportation

    def compute_customer_others(self):
        print("compute_customer_others called XXXXXXXXXXXX")
        for rec in self:
            move_lines = rec.env['account.move.line'].search([
                ('move_id.move_type', '=', 'out_invoice'),
                ('analytic_account_id', '=', rec.analytic_account_id.id),
                ('product_id.others', '=', True)])
            customer_others = 0
            for line in move_lines:
                customer_others += line.price_subtotal
            rec.customer_others = customer_others

    # @api.depends('customer_invoice_ids')
    def compute_customer_invoice_values(self):
        print("compute_customer_invoice_values called XXXXXXXXXXXXXXX")
        for rec in self:
            move_lines = rec.env['account.move.line'].search([
                ('move_id.move_type', '=', 'out_invoice'),
                ('analytic_account_id', '=', rec.analytic_account_id.id), '|', '|', '|', '|', '|', '|', '|',
                ('product_id.product_duty', '=', True),
                ('product_id.shipping_charge', '=', True),
                ('product_id.terminal_charge', '=', True),
                ('product_id.nafdac', '=', True),
                ('product_id.son', '=', True),
                ('product_id.agency', '=', True),
                ('product_id.transportation', '=', True),
                ('product_id.others', '=', True)])
            customer_invoice_ids = list(dict.fromkeys(move_lines.mapped('move_id')))
            print("<<<<<<<<<customer_invoice_ids>>>>>>>>>")
            print(customer_invoice_ids)
            customer_untaxed_value = customer_vat = customer_total_invoice_value = customer_invoice_paid = customer_invoice_unpaid = 0
            for invoice in customer_invoice_ids:
                customer_untaxed_value += invoice.amount_untaxed
                customer_vat += invoice.amount_tax
                customer_total_invoice_value += invoice.amount_total
                customer_invoice_paid += (invoice.amount_total - invoice.amount_residual)
                customer_invoice_unpaid += (invoice.amount_total - (invoice.amount_total - invoice.amount_residual))
            rec.customer_untaxed_value = customer_untaxed_value
            rec.customer_vat = customer_vat
            rec.customer_total_invoice_value = customer_total_invoice_value
            rec.customer_invoice_paid = customer_invoice_paid
            rec.customer_invoice_unpaid = customer_invoice_unpaid

    def compute_project_product_duty(self):
        print("compute_project_product_duty called XXXXXXXXXXXXXX")
        for rec in self:
            total = 0
            move_lines = rec.env['account.move.line'].search([
                ('move_id.move_type', 'in', ['in_invoice', 'in_receipt', 'out_receipt']),
                ('analytic_account_id', '=', rec.analytic_account_id.id), ('product_id.product_duty', '=', True)])
            for line in move_lines:
                total += line.price_subtotal
            expense = rec.env['hr.expense'].search([('state', 'in', ['approved', 'done']),
                                                    ('analytic_account_id', '=', rec.analytic_account_id.id),
                                                    ('product_id.product_duty', '=', True)])
            if expense:
                total += expense.total_amount
            print("<<<<<<<total>>>>>>>")
            print(total)
            rec.project_product_duty = int(total)

    def compute_project_shipping_charge(self):
        for rec in self:
            total = 0
            move_lines = rec.env['account.move.line'].search([
                ('move_id.move_type', 'in', ['in_invoice', 'in_receipt', 'out_receipt']),
                ('analytic_account_id', '=', rec.analytic_account_id.id), ('product_id.shipping_charge', '=', True)])
            for line in move_lines:
                total += line.price_subtotal
            expense = rec.env['hr.expense'].search([('state', 'in', ['approved', 'done']),
                                                    ('analytic_account_id', '=', rec.analytic_account_id.id),
                                                    ('product_id.shipping_charge', '=', True)])
            if expense:
                total += expense.total_amount
            rec.project_shipping_charge = total

    def compute_project_terminal_charge(self):
        for rec in self:
            total = 0
            move_lines = rec.env['account.move.line'].search([
                ('move_id.move_type', 'in', ['in_invoice', 'in_receipt', 'out_receipt']),
                ('analytic_account_id', '=', rec.analytic_account_id.id), ('product_id.terminal_charge', '=', True)])
            for line in move_lines:
                total += line.price_subtotal
            expense = rec.env['hr.expense'].search([('state', 'in', ['approved', 'done']),
                                                    ('analytic_account_id', '=', rec.analytic_account_id.id),
                                                    ('product_id.terminal_charge', '=', True)])
            if expense:
                total += expense.total_amount
            rec.project_terminal_charge = total

    def compute_project_nafdac(self):
        for rec in self:
            total = 0
            move_lines = rec.env['account.move.line'].search([
                ('move_id.move_type', 'in', ['in_invoice', 'in_receipt', 'out_receipt']),
                ('analytic_account_id', '=', rec.analytic_account_id.id), ('product_id.nafdac', '=', True)])
            for line in move_lines:
                total += line.price_subtotal
            expense = rec.env['hr.expense'].search([('state', 'in', ['approved', 'done']),
                                                    ('analytic_account_id', '=', rec.analytic_account_id.id),
                                                    ('product_id.nafdac', '=', True)])
            if expense:
                total += expense.total_amount

            rec.project_nafdac = total

    def compute_project_son(self):
        for rec in self:
            total = 0
            move_lines = rec.env['account.move.line'].search([
                ('move_id.move_type', 'in', ['in_invoice', 'in_receipt', 'out_receipt']),
                ('analytic_account_id', '=', rec.analytic_account_id.id), ('product_id.son', '=', True)])
            for line in move_lines:
                total += line.price_subtotal
            expense = rec.env['hr.expense'].search([('state', 'in', ['approved', 'done']),
                                                    ('analytic_account_id', '=', rec.analytic_account_id.id),
                                                    ('product_id.son', '=', True)])
            if expense:
                total += expense.total_amount
            rec.project_son = total

    def compute_project_agency(self):
        for rec in self:
            total = 0
            move_lines = rec.env['account.move.line'].search([
                ('move_id.move_type', 'in', ['in_invoice', 'in_receipt', 'out_receipt']),
                ('analytic_account_id', '=', rec.analytic_account_id.id), ('product_id.agency', '=', True)])
            for line in move_lines:
                total += line.price_subtotal
            expense = rec.env['hr.expense'].search([('state', 'in', ['approved', 'done']),
                                                    ('analytic_account_id', '=', rec.analytic_account_id.id),
                                                    ('product_id.agency', '=', True)])
            if expense:
                total += expense.total_amount
            rec.project_agency = total

    def compute_project_transportation(self):
        for rec in self:
            total = 0
            move_lines = rec.env['account.move.line'].search([
                ('move_id.move_type', 'in', ['in_invoice', 'in_receipt', 'out_receipt']),
                ('analytic_account_id', '=', rec.analytic_account_id.id), ('product_id.transportation', '=', True)])
            for line in move_lines:
                total += line.price_subtotal
            expense = rec.env['hr.expense'].search([('state', 'in', ['approved', 'done']),
                                                    ('analytic_account_id', '=', rec.analytic_account_id.id),
                                                    ('product_id.transportation', '=', True)])
            if expense:
                total += expense.total_amount
            rec.project_transportation = total

    def compute_project_others(self):
        for rec in self:
            total = 0
            move_lines = rec.env['account.move.line'].search([
                ('move_id.move_type', 'in', ['in_invoice', 'in_receipt', 'out_receipt']),
                ('analytic_account_id', '=', rec.analytic_account_id.id), ('product_id.others', '=', True)])
            for line in move_lines:
                total += line.price_subtotal
            expense = rec.env['hr.expense'].search([('state', 'in', ['approved', 'done']),
                                                    ('analytic_account_id', '=', rec.analytic_account_id.id),
                                                    ('product_id.others', '=', True)])
            if expense:
                total += expense.total_amount
            rec.project_others = total

    # smart buttons =========================>

    def compute_duty_count(self):
        for record in self:
            record.duty_move_line_ids = record.env['account.move.line'].search(
                [('analytic_account_id', '=', record.analytic_account_id.id), ('product_id.product_duty', '=', True)])
            record.duty_count = len(record.duty_move_line_ids)

    def get_duty_invoice_lines(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Duty Move Lines',
            'view_mode': 'tree',
            'res_model': 'account.move.line',
            'domain': [('analytic_account_id', '=', self.analytic_account_id.id),
                       ('product_id.product_duty', '=', True)],
            'context': "{'create': False}"
        }

    def compute_shipping_count(self):
        for record in self:
            record.shipping_move_line_ids = record.env['account.move.line'].search(
                [('analytic_account_id', '=', record.analytic_account_id.id),
                 ('product_id.shipping_charge', '=', True)])
            record.shipping_count = len(record.shipping_move_line_ids)

    def get_shipping_invoice_lines(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Shipping Move Lines',
            'view_mode': 'tree',
            'res_model': 'account.move.line',
            'domain': [('analytic_account_id', '=', self.analytic_account_id.id),
                       ('product_id.shipping_charge', '=', True)],
            'context': "{'create': False}"
        }

    def compute_terminal_count(self):
        for record in self:
            record.terminal_move_line_ids = record.env['account.move.line'].search(
                [('analytic_account_id', '=', record.analytic_account_id.id),
                 ('product_id.terminal_charge', '=', True)])
            record.terminal_count = len(record.terminal_move_line_ids)

    def get_terminal_invoice_lines(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Terminal Move Lines',
            'view_mode': 'tree',
            'res_model': 'account.move.line',
            'domain': [('analytic_account_id', '=', self.analytic_account_id.id),
                       ('product_id.terminal_charge', '=', True)],
            'context': "{'create': False}"
        }

    def compute_nafdac_count(self):
        for record in self:
            record.nafdac_move_line_ids = record.env['account.move.line'].search(
                [('analytic_account_id', '=', record.analytic_account_id.id), ('product_id.nafdac', '=', True)])
            record.nafdac_count = len(record.nafdac_move_line_ids)

    def get_nafdac_invoice_lines(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'NAFDAC Move Lines',
            'view_mode': 'tree',
            'res_model': 'account.move.line',
            'domain': [('analytic_account_id', '=', self.analytic_account_id.id), ('product_id.nafdac', '=', True)],
            'context': "{'create': False}"
        }

    def compute_son_count(self):
        for record in self:
            record.son_move_line_ids = record.env['account.move.line'].search(
                [('analytic_account_id', '=', record.analytic_account_id.id), ('product_id.son', '=', True)])
            record.son_count = len(record.son_move_line_ids)

    def get_son_invoice_lines(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'SON Move Lines',
            'view_mode': 'tree',
            'res_model': 'account.move.line',
            'domain': [('analytic_account_id', '=', self.analytic_account_id.id), ('product_id.son', '=', True)],
            'context': "{'create': False}"
        }

    def compute_agency_count(self):
        for record in self:
            record.agency_move_line_ids = record.env['account.move.line'].search(
                [('analytic_account_id', '=', record.analytic_account_id.id), ('product_id.agency', '=', True)])
            record.agency_count = len(record.agency_move_line_ids)

    def get_agency_invoice_lines(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Agency Move Lines',
            'view_mode': 'tree',
            'res_model': 'account.move.line',
            'domain': [('analytic_account_id', '=', self.analytic_account_id.id), ('product_id.agency', '=', True)],
            'context': "{'create': False}"
        }

    def compute_transportation_count(self):
        for record in self:
            record.transportation_move_line_ids = record.env['account.move.line'].search(
                [('analytic_account_id', '=', record.analytic_account_id.id), ('product_id.transportation', '=', True)])
            record.transportation_count = len(record.transportation_move_line_ids)

    def get_transportation_invoice_lines(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Transportation Move Lines',
            'view_mode': 'tree',
            'res_model': 'account.move.line',
            'domain': [('analytic_account_id', '=', self.analytic_account_id.id),
                       ('product_id.transportation', '=', True)],
            'context': "{'create': False}"
        }

    def compute_others_count(self):
        for record in self:
            record.others_move_line_ids = record.env['account.move.line'].search(
                [('analytic_account_id', '=', record.analytic_account_id.id), ('product_id.others', '=', True)])
            record.others_count = len(record.others_move_line_ids)

    def get_others_invoice_lines(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Others Move Lines',
            'view_mode': 'tree',
            'res_model': 'account.move.line',
            'domain': [('analytic_account_id', '=', self.analytic_account_id.id), ('product_id.others', '=', True)],
            'context': "{'create': False}"
        }

    def action_cb_report(self):
        for rec in self:
            move_records = self.env['account.move'].search([('move_type', '=', 'in_invoice')])
            if move_records:
                for r in move_records:
                    for fi in r.invoice_line_ids:
                        _logger.info('___ in vendor bill : ');
                        if fi.analytic_account_id.project_ids.id == rec.id:
                            rec.write({'job_vendor_bill_ids': [(4, r.id)]})
            invoice_records = self.env['account.move'].search([('move_type', '=', 'out_invoice')])
            if invoice_records:
                for i in invoice_records:
                    for i1 in i.invoice_line_ids:
                        _logger.info('___ in customer invoice : ');
                        if i1.analytic_account_id.project_ids.id == rec.id:
                            rec.write({'job_invoice_ids': [(4, i.id)]})

    # @api.depends('lib_project_com')
    # def _compute_process(self):
    #     for rec in self:
    #         total_duty = total_shipping_charge = total_terminal_charge = total_nafdac = total_son = total_agency = total_transportation = total_others = 0
    #         customer_total_duty = customer_total_shipping_charge = customer_total_terminal_charge = customer_total_nafdac = customer_total_son = customer_total_agency = customer_total_transportation = customer_total_others = invoice_untaxed_value = tax_move_line_value = paid_amount = unpaid_amount = total_invoice_value = 0
    #         demo_duty = []
    #         demo_transportation = []
    #         demo_terminal = []
    #         demo_nafdac = []
    #         demo_son = []
    #         demo_agency = []
    #         demo_others = []
    #         demo_shipping = []
    #         purchase_types = self.env['account.move'].get_purchase_types()
    #         domain = [
    #             ('move_id.state', '=', 'posted'),
    #             ('move_id.move_type', 'in', purchase_types),
    #             ('analytic_account_id', 'in', rec.analytic_account_id.ids)
    #         ]
    #         groups = self.env['account.move.line'].search(domain)
    #         move_ids = []
    #         for m in groups:
    #             move_ids.append(m.move_id)
    #         if move_ids:
    #             for v in list(set(move_ids)):
    #                 for d in v.invoice_line_ids.filtered(
    #                         lambda l: l.product_id.product_duty == True and l.analytic_account_id.id == rec.analytic_account_id.id):
    #                     for co in d:
    #                         demo_duty.append(co.id)
    #                     subtotal_duty_value = d.price_subtotal or 0.0
    #                     total_duty += subtotal_duty_value
    #                 for sh in v.invoice_line_ids.filtered(
    #                         lambda l: l.product_id.shipping_charge == True and l.analytic_account_id.id == rec.analytic_account_id.id):
    #                     for s in sh:
    #                         demo_shipping.append(s.id)
    #                     subtotal_shipping_value = sh.price_subtotal or 0.0
    #                     total_shipping_charge += subtotal_shipping_value
    #                 for t in v.invoice_line_ids.filtered(
    #                         lambda l: l.product_id.terminal_charge == True and l.analytic_account_id.id == rec.analytic_account_id.id):
    #                     for to in t:
    #                         demo_terminal.append(to.id)
    #                     subtotal_terminal_value = t.price_subtotal or 0.0
    #                     total_terminal_charge += subtotal_terminal_value
    #                 for n in v.invoice_line_ids.filtered(
    #                         lambda l: l.product_id.nafdac == True and l.analytic_account_id.id == rec.analytic_account_id.id):
    #                     for no in n:
    #                         demo_nafdac.append(no.id)
    #                     subtotal_nafdac_value = n.price_subtotal or 0.0
    #                     total_nafdac += subtotal_nafdac_value
    #                 for s in v.invoice_line_ids.filtered(
    #                         lambda l: l.product_id.son == True and l.analytic_account_id.id == rec.analytic_account_id.ids):
    #                     for so in s:
    #                         demo_son.append(so.id)
    #                     subtotal_son_value = s.price_subtotal or 0.0
    #                     total_son += subtotal_son_value
    #                 for a in v.invoice_line_ids.filtered(
    #                         lambda l: l.product_id.agency == True and l.analytic_account_id.id == rec.analytic_account_id.id):
    #                     for ao in a:
    #                         demo_agency.append(ao.id)
    #                     subtotal_agency_value = a.price_subtotal or 0.0
    #                     total_agency += subtotal_agency_value
    #                 for tr in v.invoice_line_ids.filtered(
    #                         lambda l: l.product_id.transportation == True and l.analytic_account_id.id == rec.analytic_account_id.id):
    #                     for to in tr:
    #                         demo_transportation.append(to.id)
    #                     subtotal_transportation_value = tr.price_subtotal or 0.0
    #                     total_transportation += subtotal_transportation_value
    #                 for o in v.invoice_line_ids.filtered(
    #                         lambda l: l.product_id.others == True and l.analytic_account_id.id == rec.analytic_account_id.id):
    #                     for ot in o:
    #                         demo_others.append(ot.id)
    #                     subtotal_others_value = o.price_subtotal or 0.0
    #                     total_others += subtotal_others_value
    #         if rec.job_invoice_ids:
    #             for i in rec.job_invoice_ids:
    #                 for d in i.invoice_line_ids.filtered(
    #                         lambda l: l.product_id.product_duty == True and l.analytic_account_id.id == rec.analytic_account_id.id):
    #                     subtotal_customer_duty_value = d.price_subtotal or 0.0
    #                     customer_total_duty += subtotal_customer_duty_value
    #                 for s in i.invoice_line_ids.filtered(
    #                         lambda l: l.product_id.shipping_charge == True and l.analytic_account_id.id == rec.analytic_account_id.id):
    #                     subtotal_customer_shipping_charge = s.price_subtotal or 0.0
    #                     customer_total_shipping_charge += subtotal_customer_shipping_charge
    #                 for t in i.invoice_line_ids.filtered(
    #                         lambda l: l.product_id.terminal_charge == True and l.analytic_account_id.id == rec.analytic_account_id.id):
    #                     subtotal_customer_terminal_charge = t.price_subtotal or 0.0
    #                     customer_total_terminal_charge += subtotal_customer_terminal_charge
    #                 for n in i.invoice_line_ids.filtered(
    #                         lambda l: l.product_id.nafdac == True and l.analytic_account_id.id == rec.analytic_account_id.id):
    #                     subtotal_customer_nafdac = n.price_subtotal or 0.0
    #                     customer_total_nafdac += subtotal_customer_nafdac
    #                 for so in i.invoice_line_ids.filtered(
    #                         lambda l: l.product_id.son == True and l.analytic_account_id.id == rec.analytic_account_id.id):
    #                     subtotal_customer_son = so.price_subtotal or 0.0
    #                     customer_total_son += subtotal_customer_son
    #                 for a in i.invoice_line_ids.filtered(
    #                         lambda l: l.product_id.agency == True and l.analytic_account_id.id == rec.analytic_account_id.id):
    #                     subtotal_customer_agency = a.price_subtotal or 0.0
    #                     customer_total_agency += subtotal_customer_agency
    #                 for tr in i.invoice_line_ids.filtered(
    #                         lambda l: l.product_id.transportation == True and l.analytic_account_id.id == rec.analytic_account_id.id):
    #                     subtotal_customer_transportation = tr.price_subtotal or 0.0
    #                     customer_total_transportation += subtotal_customer_transportation
    #                 for o in i.invoice_line_ids.filtered(
    #                         lambda l: l.product_id.others == True and l.analytic_account_id.id == rec.analytic_account_id.id):
    #                     subtotal_customer_others = o.price_subtotal or 0.0
    #                     customer_total_others += subtotal_customer_others
    #                 invoice_untaxed_value += i.amount_untaxed
    #                 for tx in i.invoice_line_ids.filtered(
    #                         lambda l: l.tax_ids and l.analytic_account_id.id == rec.analytic_account_id.id):
    #                     tax_move_line_value += (tx.price_subtotal * tx.tax_ids.amount) / 100
    #                 if invoice_untaxed_value or tax_move_line_value:
    #                     total_invoice_value = invoice_untaxed_value + tax_move_line_value
    #                 if i.tax_totals_json or i.amount_residual:
    #                     str_to_dict = json.loads(i.tax_totals_json)
    #                     cal_unpaid_amount = (
    #                         i.amount_residual if i.state == "posted" else str_to_dict.get("amount_total"))
    #                     paid_amount += (str_to_dict.get("amount_total") - cal_unpaid_amount)
    #                     unpaid_amount += cal_unpaid_amount
    #
    #         # value assigned to vendor bills
    #         rec.project_product_duty = total_duty
    #         rec.project_shipping_charge = total_shipping_charge
    #         rec.project_terminal_charge = total_terminal_charge
    #         rec.project_nafdac = total_nafdac
    #         rec.project_son = total_son
    #         rec.project_agency = total_agency
    #         rec.project_transportation = total_transportation
    #         rec.project_others = total_others
    #         total_cost = rec.project_product_duty + rec.project_shipping_charge + rec.project_terminal_charge + rec.project_nafdac + rec.project_son + rec.project_agency + rec.project_transportation + rec.project_others
    #         rec.write({'lib_project_com': total_cost})
    #
    #         # value assigned to the customer invoice
    #         rec.customer_duty = customer_total_duty
    #         rec.customer_shipping_charge = customer_total_shipping_charge
    #         rec.customer_terminal_charge = customer_total_terminal_charge
    #         rec.customer_nafdac = customer_total_nafdac
    #         rec.customer_son = customer_total_son
    #         rec.customer_agency = customer_total_agency
    #         rec.customer_transportation = customer_total_transportation
    #         rec.customer_others = customer_total_others
    #         rec.customer_untaxed_value = invoice_untaxed_value
    #         rec.customer_vat = tax_move_line_value
    #         rec.customer_total_invoice_value = total_invoice_value
    #         rec.total_profit = total_invoice_value - float(rec.lib_project_com)
    #         rec.customer_invoice_paid = paid_amount
    #         rec.customer_invoice_unpaid = unpaid_amount
    #         new_dict = {
    #             "duty": list(set(demo_duty)),
    #             "shipping": list(set(demo_shipping)),
    #             "terminal": list(set(demo_terminal)),
    #             "nafdac": list(set(demo_nafdac)),
    #             "son": list(set(demo_son)),
    #             "agency": list(set(demo_agency)),
    #             "transportation": list(set(demo_transportation)),
    #             "others": list(set(demo_others))
    #         }
    #         rec.duty_count = len(list(set(demo_duty)))
    #         rec.shipping_count = len(list(set(demo_shipping)))
    #         rec.terminal_count = len(list(set(demo_terminal)))
    #         rec.nafdac_count = len(list(set(demo_nafdac)))
    #         rec.son_count = len(list(set(demo_son)))
    #         rec.agency_count = len(list(set(demo_agency)))
    #         rec.transportation_count = len(list(set(demo_transportation)))
    #         rec.others_count = len(list(set(demo_others)))
    #         rec.move_line = new_dict


class AccountMoveLineExt(models.Model):
    _inherit = "account.move.line"

    project_id = fields.Many2one("project.project", "project_id")
