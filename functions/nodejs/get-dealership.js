/**
 * Get dealerships
 */

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');
const IAM_API_KEY=""
const COUCH_URL=""

async function main(params) {

    const authenticator = new IamAuthenticator({ apikey: IAM_API_KEY })
    const cloudant = CloudantV1.newInstance({
      authenticator: authenticator
    });
    cloudant.setServiceUrl(COUCH_URL);
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
