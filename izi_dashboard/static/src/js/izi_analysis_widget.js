/** @odoo-module **/
import { registry } from "@web/core/registry";
var translation = require('web.translation');
var IZIViewVisual = require('izi_dashboard.IZIViewVisual');
var _t = translation._t;
const { Component, useRef, onRendered, onPatched, onMounted } = owl;
class IZIAnalysisWidget extends Component {
    setup(){
        self = this;
        self.widgetContainer = useRef('widgetContainer');
        // self.render();
        onPatched(() => {
            self = this;
            console.log('onPatched', self.props.value);
            if (self.widgetContainer && self.widgetContainer.el) {
                var $el = $(self.widgetContainer.el);
                $el.empty();
                self.$visual = new IZIViewVisual(self, {
                    analysis_data: JSON.parse(self.props.value),
                });
                self.$visual.appendTo($el);
            }
        });
        onMounted(() => {
            self = this;
            console.log('onRendered', self.props.value);
            if (self.widgetContainer && self.widgetContainer.el) {
                var $el = $(self.widgetContainer.el);
                $el.empty();
                self.$visual = new IZIViewVisual(self, {
                    analysis_data: JSON.parse(self.props.value),
                });
                self.$visual.appendTo($el);
            }
        });
    }
}
IZIAnalysisWidget.template = 'izi_dashboard.IZIAnalysisWidget';
registry.category("fields").add("izi_analysis", IZIAnalysisWidget);