/**
 * Get dealerships
 */

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

async function main(params) {

    const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
    const cloudant = CloudantV1.newInstance({
      authenticator: authenticator
    });
    cloudant.setServiceUrl(params.COUCH_URL);
    return await getDealerships(cloudant, params);
}

async function getDealerships(cloudant, params) {
    try {
        let result = await cloudant.postFind({ db: "dealerships", selector: params });
        return {
            dealerships: result.result.docs.map(doc => {
                const { _id, _rev, ...fields } = doc;
                return fields;
                })
            };
    } catch (error) {
        return { error: error.description };
    }
}
