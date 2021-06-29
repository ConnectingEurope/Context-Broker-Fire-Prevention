var express = require('express');
var router = express.Router();
const request = require('request');
const utils = require('../../utils');


router.post('/', function (routerReq, routerRes, routerNext) {

    const b = routerReq.body;

    request({ url: getUrl(b), headers: utils.getBrokerHeaders(b), json: true }, (err, res, body) => {
        if (err) utils.sendFiwareError(routerRes, res, err);
        else {
            try {
                evaluateTypes(routerRes, b, body);
            } catch (exception) {
                if (!exception.res && !exception.err) utils.sendGenericError(routerRes, exception);
                else if (!routerRes.headersSent) {
                    utils.sendFiwareError(routerRes, exception.res, exception.err);
                }
            }
        }
    });

});

function getUrl(b) {
    // return utils.parseUrl(b.url) + '/v2/types';
    return utils.parseUrl(b.url) + '/ngsi-ld/v1/types?details=true';

}

async function evaluateTypes(routerRes, requestInfo, types) {
    const typeDtos = [];
    console.log(types);
    if (Array.isArray(types)) {
        for (const t of types) {
            typeDtos.push({
                valid: await isTypeValid(requestInfo, types),
                schema: {
                    type: t.typeName,
                    attrs: t.attributeNames,
                }
            });
        }
    }
    if (!routerRes.headersSent) routerRes.send(typeDtos);
}

async function isTypeValid(requestInfo, t) {
    return await getIsValidLocation(requestInfo, t);
}

function getIsValidLocation(requestInfo, t) {
    return new Promise((resolve, reject) => {
        const url = getValidationUrl(requestInfo, t);
        const params = getValidationParams(requestInfo, t);
        const headers = utils.getBrokerHeaders(requestInfo)
        request({ url: url, qs: params, headers: headers, json: true }, (err, res, body) => {
            console.log(body);
            if (err) reject({ res, err });
            else if (body.length > 0 && isValidLocation(body[0])) resolve(true);
            else resolve(false);
        });
    });
}

function isValidLocation(attrs) {
    // console.log(attrs.location.value.type);
    return  attrs.location.value.type === 'Point' || attrs.location.value.type === 'Polygon';
    // return attrs.length > 0 && attrs[0].type === 'Point';
}

function getValidationUrl(requestInfo, t) {
    // return utils.parseUrl(requestInfo.url) + '/v2/entities';
    return utils.parseUrl(requestInfo.url) + '/ngsi-ld/v1/entities?type=' + t.typeName;
}

function getValidationParams(requestInfo, t) {
    return {
        type: t.typeName,
        limit: 1,
        attrs: 'location',
        // options: 'values'
    }
}

module.exports = router;
