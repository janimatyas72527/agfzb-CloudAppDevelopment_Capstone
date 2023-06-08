"""IBM Cloud Function that gets all reviews for a dealership

Returns:
    List: List of reviews for the given dealership
"""
from ibmcloudant import Cloudant
from ibmcloudant import CloudantException
import requests

CONST_IAM_API_KEY = ""
CONST_COUCH_USERNAME = ""

def main(param_dict):
    """Main Function

    Args:
        param_dict (Dict): input paramater

    Returns:
        _type_: _description_ TODO
    """

    try:
        client = Cloudant.iam(
            account_name=CONST_COUCH_USERNAME,
            api_key=CONST_IAM_API_KEY,
            connect=True,
        )
        print(f"Databases: {client.all_dbs()}")
    except CloudantException as cloudant_exception:
        print("unable to connect")
        return {"error": cloudant_exception}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

    return {"dbs": client.all_dbs()}
