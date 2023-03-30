"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.requestAPI = void 0;
const coreutils_1 = require("@jupyterlab/coreutils");
const services_1 = require("@jupyterlab/services");
/**
 * Call the API extension
 *
 * @param endPoint API REST end point for the extension
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
function requestAPI(endPoint = '', init = {}) {
    return __awaiter(this, void 0, void 0, function* () {
        // Make request to Jupyter API
        const settings = services_1.ServerConnection.makeSettings();
        const requestUrl = coreutils_1.URLExt.join(settings.baseUrl, 'ipyosd', // API Namespace
        endPoint);
        let response;
        try {
            response = yield services_1.ServerConnection.makeRequest(requestUrl, init, settings);
        }
        catch (error) {
            throw new services_1.ServerConnection.NetworkError(error);
        }
        let data = yield response.text();
        if (data.length > 0) {
            try {
                data = JSON.parse(data);
            }
            catch (error) {
                console.log('Not a JSON response body.', response);
            }
        }
        if (!response.ok) {
            throw new services_1.ServerConnection.ResponseError(response, data.message || data);
        }
        return data;
    });
}
exports.requestAPI = requestAPI;
//# sourceMappingURL=handler.js.map