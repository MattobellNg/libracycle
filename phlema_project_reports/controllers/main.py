# License: Odoo Proprietary License v1.0

import json
from odoo import http
from odoo.http import content_disposition, request
from odoo.tools import html_escape


class XLSXReportController(http.Controller):
    @http.route("/report_xlsx", type="http", auth="user", methods=["POST"], csrf=False)
    def get_report_xlsx(self, model, options, output_format, token, report_name, **kw):
        uid = request.session.uid
        report_obj = request.env[model].sudo(uid)
        options = json.loads(options)

        try:
            if output_format == "xlsx":
                response = request.make_response(
                    None,
                    headers=[
                        ("Content-Type", "application/vnd.ms-excel"),
                        ("Content-Disposition", content_disposition(report_name + ".xlsx")),
                    ],
                )

                report_obj.get_xlsx_report(options, response)

            response.set_cookie("fileToken", token)

            return response

        except Exception as e:
            se = request.env["ir.http"].serialize_exception(e)
            error = {"code": 200, "message": "Odoo Server Error", "data": se}

            return request.make_response(html_escape(json.dumps(error)))
