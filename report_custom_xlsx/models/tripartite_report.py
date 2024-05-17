from collections import OrderedDict
from odoo import models, fields
from odoo.exceptions import UserError


class TripartiteReport(models.Model):

    _name = 'tripartite.report'
    _description = 'Tripartite Report'

    name = fields.Many2one('res.partner', string='Customer')
    brokers_ref = fields.Char('Broker\'s Ref')
    client_ref = fields.Char('Client Ref')
    material = fields.Char('Material')
    bank = fields.Char('Bank')
    form_m_to_bank = fields.Char('Form M To Bank')
    form_m_validated_by_bank = fields.Char('Form M Validated By Bank')
    form_m_registered_by_ncs = fields.Char('Form M Registered By NCS')
    delay_impact = fields.Char('Delay Impact')
    beneficiary = fields.Char('Beneficiary')
    lc_number = fields.Char('LC Number')
    form_m_number = fields.Char('Form M Number')
    curr = fields.Char('Curr')
    form_m_value = fields.Char('Form M Value')
    payment_mode = fields.Char('Payment Mode')
    comment = fields.Char('Comment')
    fecd_submitted = fields.Char('FECD Submitted')
    fecd_ack_copy_sent_to_gn = fields.Char('FECD ACK COPY SENT TO GN')
    date_po = fields.Char('Date P.O /Approved LOA to Broker')
    transaction_type = fields.Char('Transaction Type')
    form_m_application_to_bank = fields.Char('Form M Application to Bank')
    form_m_approved_by_customs = fields.Char('Form M Approved by Customs')
    lc_draft_shared_supplier = fields.Char('LC Draft Shared with Supplier')
    lc_draft_vetted_supplier = fields.Char('LC draft vetted by supplier')
    final_telex_received_from_bank = fields.Char(
        'Final telex received from  bank')
    final_lc_telex = fields.Char('Final LC telex / Form M sent to supplier')

    @classmethod
    def get_report_data(cls, rp):
        if not isinstance(rp, cls):
            raise UserError("Invalid object type")
        report_dict = OrderedDict()
        report_dict.update(
            serial_no=None,
            brokers_ref=rp.brokers_ref,
            client_ref=rp.client_ref,
            material=rp.material,
            bank=rp.bank,
            form_m_to_bank=rp.form_m_to_bank,
            form_m_validated_by_bank=rp.form_m_validated_by_bank,
            form_m_registered_by_ncs=rp.form_m_registered_by_ncs,
            delay_impact=rp.delay_impact,
            beneficiary=rp.beneficiary,
            lc_number=rp.lc_number,
            form_m_number=rp.form_m_number,
            curr=rp.curr,
            form_m_value=rp.form_m_value,
            payment_mode=rp.payment_mode,
            comment=rp.comment,
            fecd_submitted=rp.fecd_submitted,
            fecd_ack_copy_sent_to_gn=rp.fecd_ack_copy_sent_to_gn,
            date_po=rp.date_po,
            transaction_type=rp.transaction_type,
            form_m_application_to_bank=rp.form_m_application_to_bank,
            form_m_application_approved_by_customs=rp.form_m_approved_by_customs,
            lc_draft_shared_supplier=rp.lc_draft_shared_supplier,
            lc_draft_vetted_supplier=rp.lc_draft_vetted_supplier,
            final_telex_received_from_bank=rp.final_telex_received_from_bank,
            final_lc_telex=rp.final_lc_telex,
        )
        return report_dict
