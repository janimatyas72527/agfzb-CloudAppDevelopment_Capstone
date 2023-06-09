#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
import sys

"""IBM Cloud Function that posts a review for a dealership

Returns:
    Dict: result of the operation
"""
import requests

from ibm_cloud_sdk_core import ApiException
from ibmcloudant.cloudant_v1 import CloudantV1, Document
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def main(param_dict):
    """Main Function

    Args:
        param_dict (Dict): input paramater

    Returns:
        _type_: _description_ TODO
    """

    try:
        authenticator = IAMAuthenticator(param_dict["IAM_API_KEY"])
        service = CloudantV1(authenticator = authenticator)
        service.set_service_url(param_dict["COUCH_URL"])
    except ApiException as cloudant_exception:
        print("unable to connect")
        return {"error": cloudant_exception}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}
    body = param_dict.copy()
    del body['IAM_API_KEY']
    del body['COUCH_URL']

    review = Document.from_dict(body)
    response = service.post_document(db='reviews', document=review).get_result()
    return response
