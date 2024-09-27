from odoo import models, fields


class TrackingReportUpdate(models.TransientModel):
    _name = "custom.tracking.report.update"
    _description = "Custom Tracking Report Update"

    report_ids = fields.Many2many('custom.tracking.report', string='Reports')
    line_ids = fields.One2many('custom.tracking.report.update.line', 'update_id', string='Lines')

    def action_update(self):
        refined_data = [line._get_refined_data() for line in self.line_ids]
        return self.env['custom.tracking.report']._update_trackings(self.report_ids, refined_data)


class TrackingReportUpdateLine(models.TransientModel):
    _name = "custom.tracking.report.update.line"
    _description = "Custom Tracking Report Update Line"

    update_id = fields.Many2one('custom.tracking.report.update', string='Report Update')
    field_id = fields.Many2one('ir.model.fields', string='Field', domain="[('model_id.name', '=', 'custom.tracking.report')]") # add domain to filter by Update
    field_type = fields.Selection(related="field_id.ttype", string='Type')
    text_update = fields.Char('New Text')
    date_update = fields.Datetime('Date Update')
    boolean_update = fields.Boolean('Boolean Update')

    def _get_refined_data(self):
        for record in self:
            field_name, field_value = record.field_id.name, False 
            if record.field_id.ttype == "boolean":
                field_value = record.boolean_update
            if record.field_id.ttype == "char":
                field_value = record.text_update
            if record.field_id.ttype == "date":
                field_value = record.date_update
            return field_name, field_value
