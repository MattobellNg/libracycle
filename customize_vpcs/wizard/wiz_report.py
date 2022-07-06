from tracemalloc import start
from odoo import models,fields
from odoo.tools.misc import xlwt
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
import json

class CBReport(models.TransientModel):
    _name = 'report.customize_vpcs.report_cb_report'

    project_id = fields.Many2one('project.project',string='project')

    def generate_xlsx_report(self):
        print("print_xls_report called XXXXXXXXXXX")
        data = self.read()[0]
        return self.env.ref('customize_vpcs.action_report_cbreport_xlsx').report_action(self, data=data)
        # return {
        #     'type': 'ir.actions.report',
        #     'report_type': 'XLSX',
        #     'data': {'model': 'report.customize_vpcs.report_cb_report',
        #         'output_format': 'XLSX',
        #         'options': json.dumps(data, default=date_utils.json_default),
        #         'report_name': 'cb report',
        #     },
        # }