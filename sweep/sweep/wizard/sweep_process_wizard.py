from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)


class SweepWizard(models.TransientModel):

    _name = 'sweep.process.wizard'

    # records_to_sweep = fields.Integer("No. of Records")

    def process_sweep_scheduler(self):
        logging.info("Hamza Ilyas ----> process_sweep_scheduler Clicked on wizard")
        scheduler = self.env['ir.cron'].search([('name', '=', 'Sweep Process')])
        scheduler.method_direct_trigger()
