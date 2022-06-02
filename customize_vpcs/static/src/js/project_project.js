odoo.define('customize_vpcs.project_project', function (require) {
"use strict";

var core = require('web.core');
var FormController = require('web.FormController')

var _t = core._t;
var QWeb = core.qweb;

FormController.include({
	_onEdit: function () {
		if (this.modelName == "project.project"){
			console.log('___ this : ', this);
			if (this.renderer.state.data.check_bool){
				this._super();
			}
			var currentId = this.getSelectedIds();
   			var d = new Date();
   			var month = d.getMonth()+1;
   			var day = d.getDate();
   			var output = d.getFullYear() + '-' +
		    ((''+month).length<2 ? '0' : '') + month + '-' +
		    ((''+day).length<2 ? '0' : '') + day; 
			if (this.renderer.state.data.end_date._i == output){
				return;
			}
			else{
        		this._super();
			}
		}
		else{
			this._super();
		}
		
    },

})
});