odoo.define('phlema_project_reports.DynamicProjectReportPrint', function (require) {
    "use strict";

    var DynamicReports = require('phlema_project_reports.DynamicProjectReports');
    var core = require('web.core');
    var Qweb = core.qweb;

    var ActionManager = require('web.ActionManager');

    var framework = require('web.framework');

    var session = require('web.session');

    var rpc = require("web.rpc");

	DynamicReports.include({
		printReport: function (e) {
			var active_el = $(e.currentTarget);

			if (active_el.hasClass('print_pdf')) {
				this._printPdf();
			}
			else if	(active_el.hasClass('print_excel')) {
				this._printXlsx();
			}
		},
		_printPdf: function () {
			var r_body = this.$('.dynamic_report_body');

			var r_input = this.format_report_input();

			var r_header = "<div class='row mt16 r_header'>";

			if (r_input.date_from)
	            r_header += "<div class='col-6'>"+r_input.date_from+"</div>";
	        if (r_input.date_to)
	            r_header += "<div class='col-6'>"+r_input.date_to+"</div>";
            r_header += "</div>";

			if (r_input.journal_ids) {
				r_header += "<div class='row r_header'>";
                r_header += "<div class='col-12'>" + r_input.journal_ids + "</div>";
				r_header += "</div>";
			}

			for (var r_key in r_input) {
				if (r_input[r_key] && !['journal_ids', 'date_from', 'date_to'].includes(r_key)) {
					r_header += "<div class='row r_header'>";
                    r_header += "<div class='col-12'>" + r_input[r_key]+"</div>";
                    r_header += "</div>";
				}
			}

			var action = {
                'type': 'ir.actions.report',
                'report_type': 'qweb-pdf',
                'report_name': 'om_dynamic_reports.om_account_reports_pdf',
                'report_file': 'om_dynamic_reports.om_account_reports_pdf',
                'data': {'report_body': r_body.html(), 'r_header': r_header}
            };
            return this.do_action(action);
		},
		_printXlsx: function () {
			var r_body = this.$('.dynamic_report_body .table_r_content tr');

            var r_input = this.format_report_input();

            var lines = [], col_count = 0;
            for (var i=0;i<r_body.length;i++) {
                var temp = {};
                if (!$(r_body[i]).is(":visible"))
                    continue;
                var tds = $(r_body[i]).find('td');

                for (var j=0;j<tds.length;j++) {
                    temp[j] = {
                        name: $(tds[j]).attr('name'),
                        value: $(tds[j]).text(),
                        level: $(tds[j]).attr('level') ? $(tds[j]).attr('level').split("_")[1] : 0,
                        colspan: $(tds[j]).attr('colspan') ? $(tds[j]).attr('colspan') : 1,
                    };
                }

                lines.push(temp);
            }
            if (lines) {
                for (var i in lines[0]) {
                    col_count += parseInt(lines[0][i].colspan);
                }
            }

            framework.blockUI();

            var def = $.Deferred();

            session.get_file({
                url: '/report_xlsx',
                data: {
                    model: 'dynamic.report.config',
                    options: JSON.stringify({
                        filters: r_input,
                        lines: lines,
                        col_count: col_count,
                        report_name: this.current_report_data.account_report_id[0]
                    }),
                    output_format: 'xlsx',
                    report_name: this.current_report_data.account_report_id[1] ? this.current_report_data.account_report_id[1] : "Account Report"
                },
                success: def.resolve.bind(def),
                error: (error) => this.call('crash_manager', 'rpc_error', error),
                complete: framework.unblockUI,
            });

            return def;
		},
		format_report_input: function () {
			var r_input = {}, data = this.current_report_data;
			switch (data.account_report_id[0]) {
                case 'journals_audit': {
                    r_input.target_move = "Target moves :  " + this.get_field_label('target_move');
                    r_input.sort_selection = "Entries Sorted by :  " + this.get_field_label('sort_selection');

                    r_input.date_from = false;
                    r_input.date_to = false;
                    if (data.date_from) {
                        r_input.date_from = 'From :  ' + data.date_from;
                    }
                    if (data.date_to) {
                        r_input.date_to = 'To :  ' + data.date_to;
                    }

                    r_input.journal_ids = 'Journals :  ' + this.get_field_label('journal_ids');

                    break;
                };
                case 'partner_ledger': {
                    r_input.target_move = "Target moves :  " + this.get_field_label('target_move');
                    r_input.result_selection = "Partner's :  " + this.get_field_label('result_selection');

                    r_input.date_from = false;
                    r_input.date_to = false;
                    if (data.date_from) {
                        r_input.date_from = 'From :  ' + data.date_from;
                    }
                    if (data.date_to) {
                        r_input.date_to = 'To :  ' + data.date_to;
                    }

                    r_input.journal_ids = 'Journals :  ' + this.get_field_label('journal_ids');

                    if (data.reconciled == true) {
                        r_input.reconciled = "Showing Reconciled entries";
                    }
                    break;
                };
                case 'general_ledger': {
                    r_input.target_move = "Target moves :  " + this.get_field_label('target_move');
                    r_input.sortby = "Sort by :  " + this.get_field_label('sortby');
                    r_input.display_account = "Display accounts :  " + this.get_field_label('display_account');
                    if (data.reconciled == true) {
                        r_input.initial_balance = "Initial Balances Included";
                    }
                    r_input.date_from = false;
                    r_input.date_to = false;
                    if (data.date_from) {
                        r_input.date_from = 'From :  ' + data.date_from;
                    }
                    if (data.date_to) {
                        r_input.date_to = 'To :  ' + data.date_to;
                    }
                    r_input.journal_ids = 'Journals :  ' + this.get_field_label('journal_ids');

                    break;
                };
                case 'trial_balance': {
                    r_input.target_move = "Target moves :  " + this.get_field_label('target_move');
                    r_input.display_account = "Display accounts :  " + this.get_field_label('display_account');
                    r_input.date_from = false;
                    r_input.date_to = false;
                    if (data.date_from) {
                        r_input.date_from = 'From :  ' + data.date_from;
                    }
                    if (data.date_to) {
                        r_input.date_to = 'To :  ' + data.date_to;
                    }

                    break;
                };
                case 'aged_partner': {
                    r_input.target_move = "Target moves :  " + this.get_field_label('target_move');
                    r_input.result_selection = "Partner's :  " + this.get_field_label('result_selection');
                    r_input.date_from = false;
                    r_input.date_to = false;
                    if (data.date_from) {
                        r_input.date_from = 'From :  ' + data.date_from;
                    }
                    r_input.period_length = "Period length :  " + data.period_length;

                    break;
                };
                case 'tax_report': {
                    r_input.date_from = false;
                    r_input.date_to = false;
                    if (data.date_from) {
                        r_input.date_from = 'From :  ' + data.date_from;
                    }
                    if (data.date_to) {
                        r_input.date_to = 'To :  ' + data.date_to;
                    }
                    break;
                };
                default: {
                    r_input.target_move = "Target moves :  " + this.get_field_label('target_move');
                    if (data.debit_credit == true) {
                        r_input.debit_credit = "Showing Debit credit columns";
                    }
                    r_input.date_from = false;
                    r_input.date_to = false;
                    if (data.date_from) {
                        r_input.date_from = 'From :  ' + data.date_from;
                    }
                    if (data.date_to) {
                        r_input.date_to = 'To :  ' + data.date_to;
                    }
                }
            };
            return r_input;
		},
		get_field_label: function (field) {
			var data = this.current_report_data;
			if (field == 'target_move') {
				return data[field] == 'posted' ? 'All posted entries' : 'All Entries';
			}
			if (field == 'sort_selection') {
				return data[field] == 'move_name' ? 'Journal Entry Number' : 'Date';
			}
			if (field == 'sortby') {
				return data[field] == 'sort_date' ? 'Date' : 'Journal &amp; Partner';
			}
			if (field == 'display_account') {
				if (data[field] == 'all')
                    return 'All';
                if (data[field] == 'movement')
                    return 'With movements';
                if (data[field] == 'with_zero')
                    return 'With balance not equal to zero';
			}
			if (field == 'result_selection') {
				if (data[field] == 'customer')
					return 'Receivable accounts';
				if (data[field] == 'supplier')
					return 'Payable accounts';
				if (data[field] == 'customer_supplier')
					return 'Receivable and payable accounts';
			}
			if (field == 'journal_ids') {
				var j_names = [], j_key_ids = {};

				for (var i=0;i<this.journal_ids.length;i++) {
					j_key_ids[this.journal_ids[i].id] = this.journal_ids[i];
				}
				for (var i=0;i<data.journal_ids.length;i++) {
					j_names.push(j_key_ids[data.journal_ids[i]].name);
				}

				j_names.join(", ");

				return j_names ? j_names : "";
			}
		},
	});
});
