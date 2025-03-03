from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import fields, models, api, _

FIELD_SELECTION = [("required", "Required"), ("optional", "Optional"), ("no", "None")]

class ProjectProject(models.Model):
    _inherit = "project.project"

    project_categ_id = fields.Many2one(
        "project.project.category",
        "Job Dynamics",
        domain="[('project_type_id', '=', type_id)]",
        required=True,
    )
    has_bol_awb_ref = fields.Selection(
        selection=FIELD_SELECTION,
        string="BOL/AWB Ref",
        related="project_categ_id.has_bol_awb_ref",
        readonly=True,
        default="no",
    )
    has_job_duty = fields.Selection([], "Duty", related="project_categ_id.has_job_duty", readonly=True, default="no")
    has_custom_release_date = fields.Selection(
        [],
        "Custom Release Date",
        related="project_categ_id.has_custom_release_date",
        readonly=True,
        default="no",
    )
    has_job_tdo = fields.Selection([], "TDO", related="project_categ_id.has_job_tdo", readonly=True, default="no")
    has_terminal_rating_till = fields.Selection(
        [],
        "Terminal Rating Till",
        related="project_categ_id.has_terminal_rating_till",
        readonly=True,
        default="no",
    )
    has_etd = fields.Selection([], "ETD", related="project_categ_id.has_etd", readonly=True)
    has_eta = fields.Selection([], "ETA", related="project_categ_id.has_eta", readonly=True)
    has_ata = fields.Selection([], "ATA", related="project_categ_id.has_ata", readonly=True)
    has_rotation_number = fields.Selection(
        [],
        "Rotation Number",
        related="project_categ_id.has_rotation_number",
        readonly=True,
    )
    has_nafdac_1_stamp_date = fields.Selection(
        [],
        "NAFDAC 1st Stamp Date",
        related="project_categ_id.has_nafdac_1_stamp_date",
        readonly=True,
    )
    has_nafdac_2_stamp_date = fields.Selection(
        [],
        "NAFDAC 2nd Stamp Date",
        related="project_categ_id.has_nafdac_2_stamp_date",
        readonly=True,
    )
    has_son_date = fields.Selection([], "SON date", related="project_categ_id.has_son_date", readonly=True)
    has_free_days = fields.Selection([], "No Of Free Days", related="project_categ_id.has_free_days", readonly=True)

    @api.model
    def create(self, vals):
        result = super(ProjectProject, self).create(vals)
        if result and vals.get("project_categ_id"):
            # get project default tasks
            cat_id = vals.get("project_categ_id")
            if cat_id:
                proj_cat = self.env["project.project.category"].browse(int(cat_id))
                if proj_cat:
                    stage_ids = proj_cat.default_stage_ids.ids
                    result.write({"type_ids": [(6, 0, stage_ids)]})
                result._process_task(cat_id)

        return result

    def write(self, vals):
        if self.project_categ_id:
            if not self.type_ids:
                proj_cat = self.env["project.project.category"].browse(int(self.project_categ_id.id))
                if proj_cat:
                    stage_ids = proj_cat.default_stage_ids.ids
                    vals["type_ids"] = [(6, 0, stage_ids)]

        result = super(ProjectProject, self).write(vals)
        return result

    def _process_task(self, category_id):
        if category_id:
            proj_category_task = (
                self.env["project.task"]
                .sudo()
                .search(
                    [
                        ("project_categ_id", "=", int(category_id)),
                        ("is_category_task", "=", True),
                    ]
                )
            )
            if proj_category_task:
                for task in proj_category_task:
                    task_owner_id = task.task_assign_id.id if task.task_assign_id else False
                    task_user_id = task.task_assign_id.user_id.id if task.task_assign_id.user_id else self.user_id.id
                    task_dept = task.department_id if task.department_id else []
                    dept_id = task_dept.id if task_dept else False
                    admin_id = self.env.ref("base.user_root").id
                    if admin_id == task_user_id:
                        task_user_id = self.user_id.id
                        d_emp_rec = self.user_id._get_related_employees()
                        if d_emp_rec:
                            task_owner_id = d_emp_rec[0].id
                    if not task_owner_id and task_dept:
                        if not task_owner_id in task_dept.member_ids.ids:
                            if task_dept.manager_id:
                                task_owner_id = task_dept.manager_id.id
                                if task_owner_id:
                                    task_user_id = task_dept.manager_id.user_id.id

                    if not task_owner_id:
                        emp_rec = self.user_id._get_related_employees()
                        if emp_rec:
                            dept_id = emp_rec[0].department_id.id or False
                            task_owner_id = emp_rec[0].id
                            task_user_id = emp_rec[0].user_id.id

                    if not dept_id and task_owner_id:
                        dept_rec = self.env["hr.employee"].sudo().browse(int(task_owner_id))
                        if dept_rec:
                            dept_id = dept_rec.department_id.id if dept_rec.department_id else False

                    task_name = "%s (%s)" % (task.name, self.name)
                    # compute task start date, end date and escalation start date
                    str_dur = task.task_duration_days or 1
                    esl_dur = task.task_escalation_days or 2
                    comp_str_date = datetime.now() + relativedelta(days=int(str_dur))
                    comp_els_date = comp_str_date + relativedelta(days=int(esl_dur))
                    end_date = comp_str_date.strftime("%Y-%m-%d")
                    esl_date = comp_els_date.strftime("%Y-%m-%d")
                    task.with_context(mail_notrack=True).copy(
                        {
                            "project_id": self.id,
                            "task_assign_id": task_owner_id,
                            "user_id": task_user_id,
                            "department_id": dept_id,
                            "is_category_task": False,
                            "partner_id": self.partner_id.id,
                            "task_escalation_days": esl_dur,
                            "task_duration_days": str_dur,
                            "task_start_date": datetime.now().strftime("%Y-%m-%d"),
                            "task_end_date": end_date,
                            "date_deadline": end_date,
                            "date_assign": datetime.now().strftime("%Y-%m-%d"),
                            "task_escalation_trigger": esl_date,
                            # "creation_date": datetime.now().strftime("%Y-%m-%d"),
                            "create_date": datetime.now().strftime("%Y-%m-%d"),
                            "create_uid": self.user_id.id,
                            "name": task_name,
                        }
                    )
