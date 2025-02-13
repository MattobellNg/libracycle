from odoo import fields, models



class SweepReport(models.TransientModel):
    _name = 'sweep.report'

    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date', default=fields.Date.today)


    def print_xls_report(self):
        data = self.read()[0]
        return self.env.ref('sweep_report.action_sweep_report_xls').report_action(self, data=data)
       