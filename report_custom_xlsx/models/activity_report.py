from collections import OrderedDict
from odoo import models, fields
from odoo.exceptions import UserError


class QuotationAwaitApproval(models.Model):
    _name = 'quotation.await.approval'
    _description = 'Quotation Issued Await Approval'

    name = fields.Many2one('res.partner', string='Customer')
    brokers_reference = fields.Char('Brokers Reference')
    client_reference = fields.Char('Client Reference')
    description = fields.Char('Description')
    quantity = fields.Char('Quantity')
    c_and_f = fields.Char('C&F')
    currency = fields.Char('Currency')
    request_received = fields.Char('Request Received')
    quote_sent = fields.Char('Quote Sent')
    comment = fields.Char('Comment')

    @classmethod
    def get_report_data(cls, rp):
        if not isinstance(rp, cls):
            raise UserError("Invalid object type")
        report_dict = OrderedDict()
        report_dict.update(
            brokers_reference=rp.brokers_reference or '',
            client_reference=rp.client_reference or '',
            description=rp.description or '',
            quantity=rp.quantity or '',
            c_and_f=rp.c_and_f or '',
            currency=rp.currency or '',
            request_received=rp.request_received or '',
            quote_sent=rp.quote_sent or '',
            comment=rp.comment or '',
        )
        return report_dict


class AwaitingShipment(models.Model):
    _name = 'awaiting.shipment'
    _description = 'Awaiting Shipment'

    name = fields.Many2one('res.partner', string='Customer')
    brokers_reference = fields.Char('Brokers Reference')
    client_reference = fields.Char('Client Reference')
    description = fields.Char('Description')
    quantity = fields.Char('Quantity')
    loa_date = fields.Char('LOA Date')
    form_m_number = fields.Char('Form M number')
    form_m_applied = fields.Char('Form M Applied')
    form_m_to_supplier = fields.Char('Form M to supplier')
    etd = fields.Char('ETD')
    eta = fields.Char('ETA')
    vessel = fields.Char('Vessel')
    shipping_line = fields.Char('Shipping line')
    pod = fields.Char('POD')
    comment = fields.Char('Comment')

    @classmethod
    def get_report_data(cls, record):
        if not isinstance(record, cls):
            raise ValueError("Invalid record type")
        
        return OrderedDict(
            brokers_reference=record.brokers_reference or '',
            client_reference=record.client_reference or '',
            description=record.description or '',
            quantity=record.quantity or '',
            loa_date=record.loa_date or '',
            form_m_number=record.form_m_number or '',
            form_m_applied=record.form_m_applied or '',
            form_m_to_supplier=record.form_m_to_supplier or '',
            etd=record.etd or '',
            eta=record.eta or '',
            vessel=record.vessel or '',
            shipping_line=record.shipping_line or '',
            pod=record.pod or '',
            comment=record.comment or ''
        )


class AwaitingArrival(models.Model):
    _name = 'awaiting.arrival'
    _description = 'Awaiting Arrival'

    name = fields.Many2one('res.partner', string='Customer')
    brokers_reference = fields.Char('Brokers Reference')
    client_reference = fields.Char('Client Reference')
    description = fields.Char('Description')
    quantity = fields.Char('Quantity')
    departed = fields.Char('Departed')
    eta = fields.Char('ETA')
    vessel = fields.Char('Vessel')
    shipping_line = fields.Char('Shipping line')
    pod = fields.Char('POD')
    copy_document_date = fields.Char('Copy Document Date')
    doc_received = fields.Char('Doc Received')
    orig_docu_to_bank = fields.Char('Orig docu to bank')
    paar = fields.Char('PAAR')
    duty_receipt = fields.Char('duty receipt')
    nafdac_stamp = fields.Char('Nafdac Stamp')
    comments = fields.Char('Comments')

    @classmethod
    def get_report_data(cls, rp):
        if not isinstance(rp, cls):
            raise ValueError("Invalid object type")
        report_dict = OrderedDict()
        report_dict.update(
            brokers_reference=rp.brokers_reference or '',
            client_reference=rp.client_reference or '',
            description=rp.description or '',
            quantity=rp.quantity or '',
            departed=rp.departed or '',
            eta=rp.eta or '',
            vessel=rp.vessel or '',
            shipping_line=rp.shipping_line or '',
            pod=rp.pod or '',
            copy_document_date=rp.copy_document_date or '',
            doc_received=rp.doc_received or '',
            orig_docu_to_bank=rp.orig_docu_to_bank or '',
            paar=rp.paar or '',
            duty_receipt=rp.duty_receipt or '',
            nafdac_stamp=rp.nafdac_stamp or '',
            comments=rp.comments or '',
        )
        return report_dict


class ArrivedInClearing(models.Model):
    _name = 'arrived.in.clearing'
    _description = 'Arrived In Clearing'

    name = fields.Many2one('res.partner', string='Customer')
    brokers_reference = fields.Char('Brokers Reference')
    client_reference = fields.Char('Client Reference')
    description = fields.Char('Description')
    quantity = fields.Char('Quantity')
    berth = fields.Char('Berth')
    pod = fields.Char('POD')
    duty_receipt = fields.Char('Duty receipt')
    nafdac_stamp = fields.Char('Nafdac Stamp')
    importers_copy = fields.Char('Importer\'s copy')
    exam_started = fields.Char('Exam started')
    shipping_line_release = fields.Char('Shipping line release')
    customs_release = fields.Char('Customs release')
    tdo = fields.Char('TDO')
    delivery_instruction = fields.Char('Delivery instruction')
    delivery_started = fields.Char('Delivery started')
    delivery_completed = fields.Char('Delivery completed')
    comment = fields.Char('Comment')

    @classmethod
    def get_report_data(cls, obj):
        if not isinstance(obj, cls):
            raise ValueError("Invalid object type")
        report_dict = OrderedDict()
        report_dict.update(
            brokers_reference=obj.brokers_reference or '',
            client_reference=obj.client_reference or '',
            description=obj.description or '',
            quantity=obj.quantity or '',
            berth=obj.berth or '',
            pod=obj.pod or '',
            duty_receipt=obj.duty_receipt or '',
            nafdac_stamp=obj.nafdac_stamp or '',
            importers_copy=obj.importers_copy or '',
            exam_started=obj.exam_started or '',
            shipping_line_release=obj.shipping_line_release or '',
            customs_release=obj.customs_release or '',
            tdo=obj.tdo or '',
            delivery_instruction=obj.delivery_instruction or '',
            delivery_started=obj.delivery_started or '',
            delivery_completed=obj.delivery_completed or '',
            comment=obj.comment or '',
        )
        return report_dict


class DeliveredNotInvoiced(models.Model):
    _name = 'delivered.not.invoiced'
    _description = 'Delievered Not Invoiced'

    name = fields.Many2one('res.partner', string='Customer')
    brokers_reference = fields.Char('Brokers Reference')
    client_reference = fields.Char('Client Reference')
    description = fields.Char('Description')
    quantity = fields.Char('Quantity')
    pod = fields.Char('POD')
    duty_receipt = fields.Char('Duty receipt')
    nafdac_stamp = fields.Char('Nafdac Stamp')
    importers_copy = fields.Char('Importer\'s copy')
    exam_started = fields.Char('Exam started')
    shipping_line_release = fields.Char('Shipping line release')
    customs_release = fields.Char('Customs release')
    tdo = fields.Char('TDO')
    delivery_completed = fields.Char('Delivery completed')
    comment = fields.Char('Comment')

    @classmethod
    def get_report_data(cls, record):
        if not isinstance(record, cls):
            raise ValueError("Invalid object type")
        report_dict = OrderedDict()
        report_dict.update(
            brokers_reference=record.brokers_reference or '',
            client_reference=record.client_reference or '',
            description=record.description or '',
            quantity=record.quantity or '',
            pod=record.pod or '',
            duty_receipt=record.duty_receipt or '',
            nafdac_stamp=record.nafdac_stamp or '',
            importers_copy=record.importers_copy or '',
            exam_started=record.exam_started or '',
            shipping_line_release=record.shipping_line_release or '',
            customs_release=record.customs_release or '',
            tdo=record.tdo or '',
            delivery_completed=record.delivery_completed or '',
            comment=record.comment or '',
        )
        return report_dict


class Invoicing(models.Model):
    _name = 'activity.invoicing'
    _description = 'Invoicing'
    
    name = fields.Many2one('res.partner', string='Customer')
    brokers_reference = fields.Char('Brokers Reference')
    client_reference = fields.Char('Client Reference')
    description = fields.Char('Description')
    quantity = fields.Char('Quantity')
    delivery_completed = fields.Char('Delivery completed')
    invoice_acknowledged = fields.Char('Invoice acknowledged')
    amount_in_ngn = fields.Char('Amount in NGN')
    payment_terms = fields.Char('Payment Terms')
    expected_payment = fields.Char('Expected Payment')
    no_of_days_overdue = fields.Char('No of days overdue')
    pod = fields.Char('POD')
    comment = fields.Char('Comment')

    @classmethod
    def get_report_data(cls, invoice):
        if not isinstance(invoice, cls):
            raise ValueError("Invalid object type")
        report_dict = OrderedDict()
        report_dict.update(
            brokers_reference=invoice.brokers_reference or '',
            client_reference=invoice.client_reference or '',
            description=invoice.description or '',
            quantity=invoice.quantity or '',
            delivery_completed=invoice.delivery_completed or '',
            invoice_acknowledged=invoice.invoice_acknowledged or '',
            amount_in_ngn=invoice.amount_in_ngn or '',
            payment_terms=invoice.payment_terms or '',
            expected_payment=invoice.expected_payment or '',
            no_of_days_overdue=invoice.no_of_days_overdue or '',
            pod=invoice.pod or '',
            comment=invoice.comment or '',
        )
        return report_dict
