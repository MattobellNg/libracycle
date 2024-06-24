odoo.define("ks_custom_report.GraphModel", function(require){

    var GraphModel = require("web.GraphModel");

    GraphModel.include({

       _processData: function () {
            var self = this;
            this._super.apply(this, arguments);
            for (var i=0; i < self.chart.dataPoints.length; i++){
                if (arguments[arguments.length -1][i] && arguments[arguments.length -1][i].__domain)
                {
                    self.chart.dataPoints[i]['domain'] = arguments[arguments.length -1][i].__domain;
                }else{
                    self.chart.dataPoints[i]['domain'] = [];
                }
            }
        },

        getKsmodelDomain: function(domain){
            var self = this;
            var context = this.getSession().user_context;
            self._rpc({
                route: '/ks_custom_report/get_model_name',
                params: {
                    model: self.modelName,
                    local_context: context,
                    domain: domain,
                },
            }).then(function(result){
                if(result){
                    self.do_action(result);
                }
            })
        },

    });

    return GraphModel;
});