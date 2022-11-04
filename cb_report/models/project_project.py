from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import ValidationError
import json
import logging
_logger = logging.getLogger(__name__)


class Project(models.Model):
    _inherit = "project.project"

    lib_project_com = fields.Char(compute="_compute_process",string="Total Cost",store=False)
    wht = fields.Integer(string="WHT")

    # Total Invoice Value(N) minus Total Cost.

    total_profit = fields.Float(string="Total Profit")

    # This all fields below is for vendor bill/expense

    project_product_duty = fields.Integer(string="Duty")
    project_shipping_charge = fields.Integer(string="Shipping Charge")
    project_terminal_charge = fields.Integer(string="Terminal Charge")
    project_nafdac = fields.Integer(string="Nafdac")
    project_son = fields.Integer(string="SON")
    project_agency = fields.Integer(string="Agency")
    project_transportation = fields.Integer(string="Transportation")
    project_others = fields.Integer(string="Others")

    # This all fieds below is for customer invoice/income


    customer_duty = fields.Integer(string="Duty Income")
    customer_shipping_charge = fields.Integer(string="Customer Shipping Charge")
    customer_terminal_charge = fields.Integer(string="Customer Terminal Charge")
    customer_nafdac = fields.Integer(string="Customer Nafdac")
    customer_son = fields.Integer(string="Customer SON")
    customer_agency = fields.Integer(string="Customer Agency")
    customer_transportation = fields.Integer(string="Customer Transportation")
    customer_others = fields.Integer(string="Customer Others")
    customer_untaxed_value = fields.Integer(string="Invoice Value(N)")
    customer_vat = fields.Integer(string="VAT(N)")
    customer_total_invoice_value = fields.Integer(string="Total Invoice Value(N)")
    customer_invoice_paid = fields.Integer(string="Paid")
    customer_invoice_unpaid = fields.Integer(string="Not Paid")

    def action_cb_report(self):
        for rec in self:
            move_records = self.env['account.move'].search([('move_type','=','in_invoice')])
            if move_records:
                for r in move_records:
                    for fi in r.invoice_line_ids:
                        _logger.info('___ in vendor bill : ');
                        if fi.analytic_account_id.project_ids.id == rec.id:
                            print ('___ fi.analytic_account_id : ', fi.analytic_account_id.project_ids.id);
                            rec.write({'job_vendor_bill_ids': [(4,r.id)]})
            invoice_records = self.env['account.move'].search([('move_type','=','out_invoice')])
            if invoice_records:
                for i in invoice_records:
                    for i1 in i.invoice_line_ids:
                        _logger.info('___ in customer invoice : ');
                        if i1.analytic_account_id.project_ids.id == rec.id:
                            rec.write({'job_invoice_ids' : [(4,i.id)]})



    @api.depends('lib_project_com')
    def _compute_process(self):        
        print ('___ self : ', self);
        for rec in self:
            total_duty=total_shipping_charge=total_terminal_charge=total_nafdac=total_son=total_agency=total_transportation=total_others = 0 
            customer_total_duty=customer_total_shipping_charge=customer_total_terminal_charge=customer_total_nafdac=customer_total_son=customer_total_agency=customer_total_transportation=customer_total_others=invoice_untaxed_value=tax_move_line_value=paid_amount=unpaid_amount=total_invoice_value= 0 
            if rec.job_vendor_bill_ids:
                for v in rec.job_vendor_bill_ids:
                    for d in v.invoice_line_ids.filtered(lambda l: l.product_id.product_duty == True):
                        subtotal_duty_value = d.price_subtotal or 0.0
                        total_duty += subtotal_duty_value
                    for sh in v.invoice_line_ids.filtered(lambda l: l.product_id.shipping_charge == True):
                        subtotal_shipping_value = sh.price_subtotal or 0.0
                        total_shipping_charge += subtotal_shipping_value
                    for t in v.invoice_line_ids.filtered(lambda l: l.product_id.terminal_charge == True):                        
                        subtotal_terminal_value = t.price_subtotal or 0.0
                        total_terminal_charge += subtotal_terminal_value
                    for n in v.invoice_line_ids.filtered(lambda l: l.product_id.nafdac == True):
                        subtotal_nafdac_value = n.price_subtotal or 0.0
                        total_nafdac += subtotal_nafdac_value
                    for s in v.invoice_line_ids.filtered(lambda l: l.product_id.son == True):
                        subtotal_son_value = s.price_subtotal or 0.0
                        total_son += subtotal_son_value
                    for a in v.invoice_line_ids.filtered(lambda l: l.product_id.agency == True):
                        subtotal_agency_value = a.price_subtotal or 0.0
                        total_agency += subtotal_agency_value
                    for tr in v.invoice_line_ids.filtered(lambda l: l.product_id.transportation == True):
                        subtotal_transportation_value = tr.price_subtotal or 0.0
                        total_transportation += subtotal_transportation_value
                    for o in v.invoice_line_ids.filtered(lambda l: l.product_id.others == True):
                        subtotal_others_value = o.price_subtotal or 0.0
                        total_others += subtotal_others_value
            if rec.job_invoice_ids:
                for i in rec.job_invoice_ids:
                    print ('___ i : ', i);
                    for d in i.invoice_line_ids.filtered(lambda l: l.product_id.product_duty == True):
                        subtotal_customer_duty_value = d.price_subtotal or 0.0
                        customer_total_duty += subtotal_customer_duty_value
                    for s in  i.invoice_line_ids.filtered(lambda l: l.product_id.shipping_charge == True):
                        subtotal_customer_shipping_charge = s.price_subtotal or 0.0
                        customer_total_shipping_charge += subtotal_customer_shipping_charge
                    for t in i.invoice_line_ids.filtered(lambda l: l.product_id.terminal_charge == True):
                        subtotal_customer_terminal_charge = t.price_subtotal or 0.0
                        customer_total_terminal_charge += subtotal_customer_terminal_charge
                    for n in i.invoice_line_ids.filtered(lambda l: l.product_id.nafdac == True):
                        subtotal_customer_nafdac = n.price_subtotal or 0.0
                        customer_total_nafdac += subtotal_customer_nafdac
                    for so in  i.invoice_line_ids.filtered(lambda l: l.product_id.son == True):
                        subtotal_customer_son = so.price_subtotal or 0.0
                        customer_total_son += subtotal_customer_son
                    for a in i.invoice_line_ids.filtered(lambda l: l.product_id.agency == True):
                        subtotal_customer_agency = a.price_subtotal or 0.0
                        customer_total_agency += subtotal_customer_agency
                    for tr in i.invoice_line_ids.filtered(lambda l: l.product_id.transportation == True):
                        subtotal_customer_transportation = tr.price_subtotal or 0.0
                        customer_total_transportation += subtotal_customer_transportation
                    for o in i.invoice_line_ids.filtered(lambda l: l.product_id.others == True):
                        subtotal_customer_others = o.price_subtotal or 0.0
                        customer_total_others += subtotal_customer_others                    
                    invoice_untaxed_value += i.amount_untaxed
                    for tx in i.invoice_line_ids.filtered(lambda l: l.tax_ids):
                        tax_move_line_value += tx.price_subtotal or 0.0
                    if invoice_untaxed_value or tax_move_line_value:
                        total_invoice_value = invoice_untaxed_value + tax_move_line_value
                    if i.tax_totals_json or i.amount_residual:
                        str_to_dict = json.loads(i.tax_totals_json)
                        cal_unpaid_amount = (i.amount_residual if i.state == "posted" else str_to_dict.get("amount_total"))
                        print ('___ cal_unpaid_amount : ', cal_unpaid_amount);
                        paid_amount += (str_to_dict.get("amount_total") - cal_unpaid_amount)
                        print ('___ paid_amount : ', paid_amount);
                        unpaid_amount += cal_unpaid_amount
                        print ('___ unpaid_amount : ', unpaid_amount);



            print ('___ Total paid_amount : ', paid_amount);
            print ('___ Total unpaid_amount : ', unpaid_amount);
            # value assigned to vendor bills
            rec.project_product_duty = total_duty
            rec.project_shipping_charge = total_shipping_charge
            rec.project_terminal_charge = total_terminal_charge
            rec.project_nafdac = total_nafdac
            rec.project_son = total_son
            rec.project_agency = total_agency
            rec.project_transportation = total_transportation
            rec.project_others = total_others
            total_cost = rec.project_product_duty + rec.project_shipping_charge + rec.project_terminal_charge + rec.project_nafdac + rec.project_son + rec.project_agency + rec.project_transportation + rec.project_others    
            rec.write({'lib_project_com':total_cost})

            # value assigned to the customer invoice
            rec.customer_duty = customer_total_duty
            rec.customer_shipping_charge = customer_total_shipping_charge
            rec.customer_terminal_charge = customer_total_terminal_charge
            rec.customer_nafdac = customer_total_nafdac
            rec.customer_son = customer_total_son
            rec.customer_agency = customer_total_agency
            rec.customer_transportation = customer_total_transportation
            rec.customer_others = customer_total_others
            rec.customer_untaxed_value = invoice_untaxed_value
            rec.customer_vat = tax_move_line_value
            rec.customer_total_invoice_value = total_invoice_value
            rec.total_profit = total_invoice_value - int(rec.lib_project_com)
            rec.customer_invoice_paid = paid_amount
            rec.customer_invoice_unpaid = unpaid_amount