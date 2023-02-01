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
    project_terminal_charge = fields.Float(string="Terminal Charge")
    project_terminal_charge = fields.float(string="Terminal Charge")
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


    # For Smart Buttons

    duty_count = fields.Integer(string="Duty Invoice Line")
    shipping_count = fields.Integer(string="Shipping Invoice Line")
    terminal_count = fields.Integer(string="Terminal Invoice Line")
    nafdac_count = fields.Integer(string="Nafdac Invoice Line")
    son_count = fields.Integer(string="Son Invoice Line")
    agency_count = fields.Integer(string="Agency Invoice Line")
    transportation_count = fields.Integer(string="Transportation Invoice Line")
    others_count = fields.Integer(string="Others Invoice Line")

    move_line = fields.Char(string="Transportation Move Line")

    def _compute_duty_invoice_line(self):
        for pro in self:
            pro.duty_count=pro.shipping_count=pro.terminal_count=pro.nafdac_count=pro.son_count=pro.agency_count=pro.transportation_count=pro.others_count = 0

    def duty_invoice_line(self):
        dy_value = self._context.get('button')
        self.ensure_one()
        action = self.env.ref("account.action_account_moves_all_tree")
        json_move_line = json.loads(self.move_line.replace("'",'"'))
        return {
            "name": action.name,
            "type": action.type,
            "domain": [['id', 'in', json_move_line.get(dy_value)]],
            "view_mode": "tree,form",
            "res_model": action.res_model,
        }

    def action_cb_report(self):
        for rec in self:
            move_records = self.env['account.move'].search([('move_type','=','in_invoice')])
            if move_records:
                for r in move_records:
                    for fi in r.invoice_line_ids:
                        _logger.info('___ in vendor bill : ');
                        if fi.analytic_account_id.project_ids.id == rec.id:
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
        for rec in self:
            total_duty=total_shipping_charge=total_terminal_charge=total_nafdac=total_son=total_agency=total_transportation=total_others = 0 
            customer_total_duty=customer_total_shipping_charge=customer_total_terminal_charge=customer_total_nafdac=customer_total_son=customer_total_agency=customer_total_transportation=customer_total_others=invoice_untaxed_value=tax_move_line_value=paid_amount=unpaid_amount=total_invoice_value= 0 
            demo_duty = []
            demo_transportation= []
            demo_terminal=[]
            demo_nafdac= []
            demo_son= []
            demo_agency= []
            demo_others=[]
            demo_shipping = []
            purchase_types = self.env['account.move'].get_purchase_types()
            domain = [
                ('move_id.state', '=', 'posted'),
                ('move_id.move_type', 'in', purchase_types),
                ('analytic_account_id', 'in', rec.analytic_account_id.ids)
            ]
            groups = self.env['account.move.line'].search(domain)
            move_ids = []
            for m in groups:
                move_ids.append(m.move_id)
            if move_ids:
                for v in list(set(move_ids)):
                    for d in v.invoice_line_ids.filtered(lambda l: l.product_id.product_duty == True and l.analytic_account_id.id == rec.analytic_account_id.id):
                        for co in d:
                            demo_duty.append(co.id)
                        subtotal_duty_value = d.price_subtotal or 0.0
                        total_duty += subtotal_duty_value
                    for sh in v.invoice_line_ids.filtered(lambda l: l.product_id.shipping_charge == True and l.analytic_account_id.id == rec.analytic_account_id.id):
                        for s in sh:
                            demo_shipping.append(s.id)
                        subtotal_shipping_value = sh.price_subtotal or 0.0
                        total_shipping_charge += subtotal_shipping_value
                    for t in v.invoice_line_ids.filtered(lambda l: l.product_id.terminal_charge == True and l.analytic_account_id.id == rec.analytic_account_id.id):                                             
                        for to in t:
                            demo_terminal.append(to.id)
                        subtotal_terminal_value = t.price_subtotal or 0.0
                        total_terminal_charge += subtotal_terminal_value
                    for n in v.invoice_line_ids.filtered(lambda l: l.product_id.nafdac == True and l.analytic_account_id.id == rec.analytic_account_id.id):
                        for no in n:
                            demo_nafdac.append(no.id)
                        subtotal_nafdac_value = n.price_subtotal or 0.0
                        total_nafdac += subtotal_nafdac_value
                    for s in v.invoice_line_ids.filtered(lambda l: l.product_id.son == True and l.analytic_account_id.id == rec.analytic_account_id.ids):
                        for so in s:
                            demo_son.append(so.id)
                        subtotal_son_value = s.price_subtotal or 0.0
                        total_son += subtotal_son_value
                    for a in v.invoice_line_ids.filtered(lambda l: l.product_id.agency == True and l.analytic_account_id.id == rec.analytic_account_id.id):
                        for ao in a:
                            demo_agency.append(ao.id)
                        subtotal_agency_value = a.price_subtotal or 0.0
                        total_agency += subtotal_agency_value
                    for tr in v.invoice_line_ids.filtered(lambda l: l.product_id.transportation == True and l.analytic_account_id.id == rec.analytic_account_id.id):
                        for to in tr:
                            demo_transportation.append(to.id)
                        subtotal_transportation_value = tr.price_subtotal or 0.0
                        total_transportation += subtotal_transportation_value
                    for o in v.invoice_line_ids.filtered(lambda l: l.product_id.others == True and l.analytic_account_id.id == rec.analytic_account_id.id):
                        for ot in o:
                            demo_others.append(ot.id)
                        subtotal_others_value = o.price_subtotal or 0.0
                        total_others += subtotal_others_value
            if rec.job_invoice_ids:
                for i in rec.job_invoice_ids:
                    for d in i.invoice_line_ids.filtered(lambda l: l.product_id.product_duty == True and l.analytic_account_id.id == rec.analytic_account_id.id):
                        subtotal_customer_duty_value = d.price_subtotal or 0.0
                        customer_total_duty += subtotal_customer_duty_value
                    for s in  i.invoice_line_ids.filtered(lambda l: l.product_id.shipping_charge == True and l.analytic_account_id.id == rec.analytic_account_id.id):
                        subtotal_customer_shipping_charge = s.price_subtotal or 0.0
                        customer_total_shipping_charge += subtotal_customer_shipping_charge
                    for t in i.invoice_line_ids.filtered(lambda l: l.product_id.terminal_charge == True and l.analytic_account_id.id == rec.analytic_account_id.id):
                        subtotal_customer_terminal_charge = t.price_subtotal or 0.0
                        customer_total_terminal_charge += subtotal_customer_terminal_charge
                    for n in i.invoice_line_ids.filtered(lambda l: l.product_id.nafdac == True and l.analytic_account_id.id == rec.analytic_account_id.id):
                        subtotal_customer_nafdac = n.price_subtotal or 0.0
                        customer_total_nafdac += subtotal_customer_nafdac
                    for so in  i.invoice_line_ids.filtered(lambda l: l.product_id.son == True and l.analytic_account_id.id == rec.analytic_account_id.id):
                        subtotal_customer_son = so.price_subtotal or 0.0
                        customer_total_son += subtotal_customer_son
                    for a in i.invoice_line_ids.filtered(lambda l: l.product_id.agency == True and l.analytic_account_id.id == rec.analytic_account_id.id):
                        subtotal_customer_agency = a.price_subtotal or 0.0
                        customer_total_agency += subtotal_customer_agency
                    for tr in i.invoice_line_ids.filtered(lambda l: l.product_id.transportation == True and l.analytic_account_id.id == rec.analytic_account_id.id):
                        subtotal_customer_transportation = tr.price_subtotal or 0.0
                        customer_total_transportation += subtotal_customer_transportation
                    for o in i.invoice_line_ids.filtered(lambda l: l.product_id.others == True and l.analytic_account_id.id == rec.analytic_account_id.id):
                        subtotal_customer_others = o.price_subtotal or 0.0
                        customer_total_others += subtotal_customer_others                    
                    invoice_untaxed_value += i.amount_untaxed
                    for tx in i.invoice_line_ids.filtered(lambda l: l.tax_ids and l.analytic_account_id.id == rec.analytic_account_id.id):
                        tax_move_line_value += (tx.price_subtotal*tx.tax_ids.amount)/100
                    if invoice_untaxed_value or tax_move_line_value:
                        total_invoice_value = invoice_untaxed_value + tax_move_line_value
                    if i.tax_totals_json or i.amount_residual:
                        str_to_dict = json.loads(i.tax_totals_json)
                        cal_unpaid_amount = (i.amount_residual if i.state == "posted" else str_to_dict.get("amount_total"))
                        paid_amount += (str_to_dict.get("amount_total") - cal_unpaid_amount)
                        unpaid_amount += cal_unpaid_amount

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
            rec.total_profit = total_invoice_value - float(rec.lib_project_com)
            rec.total_profit = total_invoice_value - int(rec.lib_project_com)
            rec.customer_invoice_paid = paid_amount
            rec.customer_invoice_unpaid = unpaid_amount
            new_dict = {
                "duty" : list(set(demo_duty)),
                "shipping" : list(set(demo_shipping)),
                "terminal" : list(set(demo_terminal)),
                "nafdac" : list(set(demo_nafdac)),
                "son" : list(set(demo_son)),
                "agency" : list(set(demo_agency)),
                "transportation" : list(set(demo_transportation)),
                "others" : list(set(demo_others))
            }
            rec.duty_count = len(list(set(demo_duty)))
            rec.shipping_count = len(list(set(demo_shipping)))
            rec.terminal_count = len(list(set(demo_terminal)))
            rec.nafdac_count = len(list(set(demo_nafdac)))
            rec.son_count = len(list(set(demo_son)))
            rec.agency_count = len(list(set(demo_agency)))
            rec.transportation_count = len(list(set(demo_transportation)))
            rec.others_count = len(list(set(demo_others)))
            rec.move_line = new_dict