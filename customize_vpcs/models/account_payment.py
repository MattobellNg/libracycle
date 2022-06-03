from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import ValidationError


class AccountPayment(models.Model):
    _inherit = "account.payment"

    def write(self,vals):
        data = super(AccountPayment, self).write(vals)
        get_department_id = self.env['hr.department'].search([('name','=','QAC')])
        get_employee_id = self.env['hr.employee'].search([('department_id','=',get_department_id.id)])
        if vals: 
            data = 'record id=%s changed.\n\n'%(self.id)
            for key in vals:
                data += '%s --> %s \n\n,'%(key,vals[key])
            for emp in get_employee_id:                        
                send_message = emp.message_post(body=data)
        return data