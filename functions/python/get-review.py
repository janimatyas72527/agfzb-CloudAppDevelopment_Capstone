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

"""IBM Cloud Function that gets all reviews for a dealership

Returns:
    List: List of reviews for the given dealership
"""
import requests

from ibm_cloud_sdk_core import ApiException
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def clean_doc(doc):
    del doc['_id']
    del doc['_rev']
    return doc

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
    sel = param_dict.copy()
    del sel['IAM_API_KEY']
    del sel['COUCH_URL']
    reviews = service.post_find('reviews', sel).get_result()['docs']
    reviews = map(clean_doc, reviews)
    return { "reviews": list(reviews) }
