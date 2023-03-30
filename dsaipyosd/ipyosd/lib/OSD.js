"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.OSDMainView = exports.OSDModel = void 0;
const base_1 = require("@jupyter-widgets/base");
const openseadragon_1 = require("openseadragon");
const version_1 = require("./version");
class OSDModel extends base_1.DOMWidgetModel {
    defaults() {
        return Object.assign(Object.assign({}, super.defaults()), { _model_name: OSDModel.model_name, _model_module: OSDModel.model_module, _model_module_version: OSDModel.model_module_version, _view_name: OSDModel.view_name, _view_module: OSDModel.view_module, _view_module_version: OSDModel.view_module_version });
    }
}
exports.OSDModel = OSDModel;
OSDModel.serializers = Object.assign({}, base_1.DOMWidgetModel.serializers);
OSDModel.model_name = 'OSDModel';
OSDModel.model_module = version_1.MODULE_NAME;
OSDModel.model_module_version = version_1.MODULE_VERSION;
OSDModel.view_name = 'OSDMainView';
OSDModel.view_module = version_1.MODULE_NAME;
OSDModel.view_module_version = version_1.MODULE_VERSION;
class OSDMainView extends base_1.DOMWidgetView {
    constructor(options) {
        super(options);
        this.value_changed = () => {
            this.el.classList.add('jupyter-widgets');
            this.el.classList.add('iiif-container');
            this._viewer = new openseadragon_1.Viewer({
                element: this.el,
                prefixUrl: "/view/iiif/static/images/",
                preserveViewport: true,
                visibilityRatio: 1,
                minZoomLevel: 1,
                defaultZoomLevel: 1,
                sequenceMode: true,
                showNavigationControl: false,
                tileSources: [
                    this.model.get('url')
                ]
            });
        };
        //        this._viewer = null;
    }
    render() {
        //		OSDMainView.__super__.render.apply(this, arguments);
        this.value_changed();
        this.model.on('change:value', this.value_changed, this);
    }
}
exports.OSDMainView = OSDMainView;
//# sourceMappingURL=OSD.js.map