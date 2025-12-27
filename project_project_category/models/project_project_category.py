# © 2016-2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, _


FIELD_SELECTION = [("required", "Required"), ("optional", "Optional"), ("no", "None")]


class ProjectProjectCategory(models.Model):
    _name = "project.project.category"

    name = fields.Char("Name", required=True, translate=True, select=True)
    description = fields.Char("Description", translate=True)
    active = fields.Boolean("Active", default=True)
    project_type_id = fields.Many2one("project.type", "Project Type", required=False)
    default_task_count = fields.Integer(compute="_compute_default_task_count", string="Default Tasks")
    task_count = fields.Integer(compute="_compute_task_count", string="Tasks")

    task_needaction_count = fields.Integer(compute="_compute_task_needaction_count", string="Tasks")
    project_category_task_ids = fields.One2many("project.task", "project_categ_id", string="Project Default Tasks")
    default_stage_ids = fields.Many2many("project.task.type", string="Default Stages")
    has_bol_awb_ref = fields.Selection(
        FIELD_SELECTION,
        "BOL/AWB Ref",
        required=True,
        default="optional",
        help="Display BOL/AWB Ref on project",
    )
    has_job_duty = fields.Selection(
        FIELD_SELECTION,
        "Duty",
        required=True,
        default="no",
        help="Display Duty field on project",
    )
    has_custom_release_date = fields.Selection(
        FIELD_SELECTION,
        "Custom Release Date",
        required=True,
        default="no",
        help="Display Custom Release Date field on project",
    )
    has_job_tdo = fields.Selection(
        FIELD_SELECTION,
        "TDO",
        required=True,
        default="no",
        help="Display TDO field on project",
    )

    has_terminal_rating_till = fields.Selection(
        FIELD_SELECTION,
        "Terminal Rating Till",
        required=True,
        default="no",
        help="Display Terminal Rating Till field on project",
    )
    has_etd = fields.Selection(
        FIELD_SELECTION,
        "ETD",
        required=True,
        default="optional",
        help="Display ETD section on project",
    )
    has_eta = fields.Selection(
        FIELD_SELECTION,
        "ETA",
        required=True,
        default="optional",
        help="Display ETA section on project",
    )
    has_ata = fields.Selection(
        FIELD_SELECTION,
        "ATA",
        required=True,
        default="no",
        help="Display ATA section on project",
    )
    has_rotation_number = fields.Selection(
        FIELD_SELECTION,
        "Rotation Number",
        required=True,
        default="no",
        help="Display rotation number section on project",
    )
    has_nafdac_1_stamp_date = fields.Selection(
        FIELD_SELECTION,
        "NAFDAC 1st Stamp Date",
        required=True,
        default="no",
        help="Display NAFDAC 1st Stamp Date section on project",
    )
    has_nafdac_2_stamp_date = fields.Selection(
        FIELD_SELECTION,
        "NAFDAC 2nd Stamp Date",
        required=True,
        default="no",
        help="Display NAFDAC 2nd stamp date section on project",
    )
    has_son_date = fields.Selection(
        FIELD_SELECTION,
        "SON date",
        required=True,
        default="no",
        help="Display SON date section on project",
    )
    has_free_days = fields.Selection(
        FIELD_SELECTION,
        "No Of Free Days",
        required=True,
        default="optional",
        help="Display POD section on project",
    )

    _order = "name"

    _sql_constraints = [
        ("name_uniq", "UNIQUE (name)", "Name already exists."),
    ]

    def _compute_default_task_count(self):
        for project in self:
            default_task = self.env["project.task"].search(
                [("is_category_task", "=", True), ("project_categ_id", "=", project.id)]
            )
            project.default_task_count = len(default_task)

    def _compute_task_count(self):
        for project in self:
            task = project.project_category_task_ids.search(
                [
                    ("project_categ_id", "=", project.id),
                    ("is_category_task", "=", False),
                ]
            )
            project.task_count = len(task)

    def _compute_task_needaction_count(self):
        projects_data = self.env["project.task"].read_group(
            [("project_categ_id", "in", self.ids), ("message_needaction", "=", True)],
            ["project_categ_id"],
            ["project_categ_id"],
        )
        mapped_data = {
            project_data["project_categ_id"][0]: int(project_data["project_categ_id_count"])
            for project_data in projects_data
        }
        for project in self:
            project.task_needaction_count = mapped_data.get(project.id, 0)


