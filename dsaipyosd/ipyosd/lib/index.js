"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", { value: true });
const base = __importStar(require("@jupyter-widgets/base"));
const version_1 = require("./version");
const OSD_1 = require("./OSD");
const handler_1 = require("./handler");
/**
 * Initialization data for the ipyosd extension.
 */
const extension = {
    id: 'ipyosd',
    requires: [base.IJupyterWidgetRegistry],
    autoStart: true,
    activate: activate
};
function activate(app, widgets) {
    console.log('JupyterLab extension ipyosd is activated!');
    handler_1.requestAPI('get_example')
        .then(data => {
        console.log(data);
    })
        .catch(reason => {
        console.error(`The ipyosd server extension appears to be missing.\n${reason}`);
    });
    widgets.registerWidget({
        name: "ipyosd",
        version: version_1.MODULE_VERSION,
        exports: {
            OSDModel: OSD_1.OSDModel,
            OSDMainView: OSD_1.OSDMainView,
        },
    });
}
;
exports.default = extension;
//# sourceMappingURL=index.js.map