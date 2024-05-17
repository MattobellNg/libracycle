from collections import OrderedDict
from odoo import models, fields
from odoo.exceptions import UserError


class MonthlyInvoicingReport(models.Model):

    _name = 'monthly_invoicing.report'
    _description = 'Monthly Invoicing Report'

    name = fields.Many2one('res.partner', string='Customer')
    file_ref = fields.Char('File Ref')
    po_ref = fields.Char('PO Ref')
    client_ref = fields.Char('Client Ref')
    conf_dt = fields.Char('Conf Dt')
    invoice_dt = fields.Char('Invoice Dt')
    supplier_name = fields.Char('supplier_name')
    goods_description = fields.Char('Goods Description')
    twenty_inch = fields.Char('20"')
    forty_inch = fields.Char('40"')
    kgs = fields.Char('Kgs')
    units = fields.Char('Units')
    cnf_value = fields.Char('CNF Value')
    cur = fields.Char('CUR')
    duty = fields.Char('Duty')
    port_levy = fields.Char('Port Levy')
    ciss = fields.Char('CISS')
    etls = fields.Char('ETLS')
    excise = fields.Char('Excise / SPl Levy')
    vat_on_duty = fields.Char('VAT on Duty')
    terminal_charges = fields.Char('Terminal Charges')
    terminal_rent = fields.Char('Terminal Rent')
    shipping_line_charges = fields.Char('Shipping Line Charges')
    shipping_dem = fields.Char('Shipping Dem')
    provisional_dem = fields.Char('Provisional Dem')
    container_deposit = fields.Char('Container deposit')
    airport_charges = fields.Char('Airport Charges')
    truck_dem = fields.Char('Truck Dem')
    nesrea = fields.Char('NESREA / NASSIMA / Practitioner fee')
    quarantine = fields.Char('QUARANTINE')
    son = fields.Char('SON')
    nafdac = fields.Char('NAFDAC')
    brokers_fee = fields.Char('Brokers Fee')
    agency_fee = fields.Char('Agency Fee / Fastrack')
    insurance = fields.Char('Insurance')
    transport = fields.Char('Transport')
    finance_cost = fields.Char('Finance Cost')
    acc_main_fee = fields.Char('Acc Main. Fee')
    vat = fields.Char('VAT')
    total = fields.Char('Total')
    c_number = fields.Char('C Number')
    mode_of_clearing = fields.Char('Mode of Clearing')

    @classmethod
    def get_report_data(cls, rp):
        if not isinstance(rp, cls):
            raise UserError("Invalid object type")
        report_dict = OrderedDict()
        report_dict.update(
            file_ref=rp.file_ref,
            po_ref=rp.po_ref,
            client_ref=rp.client_ref,
            conf_dt=rp.conf_dt,
            invoice_dt=rp.invoice_dt,
            supplier_name=rp.supplier_name,
            goods_description=rp.goods_description,
            twenty_inch=rp.twenty_inch,
            forty_inch=rp.forty_inch,
            kgs=rp.kgs,
            units=rp.units,
            cnf_value=rp.cnf_value,
            cur=rp.cur,
            duty=rp.duty,
            port_levy=rp.port_levy,
            ciss=rp.ciss,
            etls=rp.etls,
            excise=rp.excise,
            vat_on_duty=rp.vat_on_duty,
            terminal_charges=rp.terminal_charges,
            terminal_rent=rp.terminal_rent,
            shipping_line_charges=rp.shipping_line_charges,
            shipping_dem=rp.shipping_dem,
            provisional_dem=rp.provisional_dem,
            container_deposit=rp.container_deposit,
            airport_charges=rp.airport_charges,
            truck_dem=rp.truck_dem,
            nesrea=rp.nesrea,
            quarantine=rp.quarantine,
            son=rp.son,
            nafdac=rp.nafdac,
            brokers_fee=rp.brokers_fee,
            agency_fee=rp.agency_fee,
            insurance=rp.insurance,
            transport=rp.transport,
            finance_cost=rp.finance_cost,
            acc_main_fee=rp.acc_main_fee,
            vat=rp.vat,
            total=rp.total,
            c_number=rp.c_number,
            mode_of_clearing=rp.mode_of_clearing,
        )
        return report_dict
