import json
import http.client
from datetime import datetime
from .models import CarDealer, DealerReview

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))

def get_request(package_name, action_name, params):
    try:
        host = 'eu-gb.functions.cloud.ibm.com'
        namespace = '4a329e9a-d171-4f4b-b90c-cbb0435b8cc8'

        conn = http.client.HTTPSConnection(host)

        headers = {
            'accept': "application/json",
            'authorization': "Bearer eyJraWQiOiIyMDIzMDUxMTA4MzEiLCJhbGciOiJSUzI1NiJ9.eyJpYW1faWQiOiJJQk1pZC0zMTAwMDBBUDVYIiwiaWQiOiJJQk1pZC0zMTAwMDBBUDVYIiwicmVhbG1pZCI6IklCTWlkIiwianRpIjoiNTlmMjI4MjYtNTE1OS00MjBlLWFiNjEtYmE1ZDU5YWIzNTMyIiwiaWRlbnRpZmllciI6IjMxMDAwMEFQNVgiLCJnaXZlbl9uYW1lIjoiTWF0eWFzIiwiZmFtaWx5X25hbWUiOiJKYW5pIiwibmFtZSI6Ik1hdHlhcyBKYW5pIiwiZW1haWwiOiJqYW5pLm1hdHlhc0BnbWFpbC5jb20iLCJzdWIiOiJqYW5pLm1hdHlhc0BnbWFpbC5jb20iLCJhdXRobiI6eyJzdWIiOiJqYW5pLm1hdHlhc0BnbWFpbC5jb20iLCJpYW1faWQiOiJJQk1pZC0zMTAwMDBBUDVYIiwibmFtZSI6Ik1hdHlhcyBKYW5pIiwiZ2l2ZW5fbmFtZSI6Ik1hdHlhcyIsImZhbWlseV9uYW1lIjoiSmFuaSIsImVtYWlsIjoiamFuaS5tYXR5YXNAZ21haWwuY29tIn0sImFjY291bnQiOnsidmFsaWQiOnRydWUsImJzcyI6IjVhMzk1ODJkNWE4NjRjYzM5YjYzYzMwY2VlMDU2YmZjIiwiaW1zX3VzZXJfaWQiOiIxMDgxMDQzMyIsImltcyI6IjI2MzI3NTUifSwiaWF0IjoxNjg2MzE2Nzg4LCJleHAiOjE2ODYzMjAzODgsImlzcyI6Imh0dHBzOi8vaWFtLmNsb3VkLmlibS5jb20vaWRlbnRpdHkiLCJncmFudF90eXBlIjoidXJuOmlibTpwYXJhbXM6b2F1dGg6Z3JhbnQtdHlwZTpwYXNzY29kZSIsInNjb3BlIjoiaWJtIG9wZW5pZCIsImNsaWVudF9pZCI6ImJ4IiwiYWNyIjoxLCJhbXIiOlsicHdkIl19.cU4x6eGVlHpkrJam5mrKFksGSWZ5kzEhVyJkB2U-Rkcmp0_GqehmhVPGVrgwoHHX1_shDfrJwS2pmsUcaq3aD8ZUUI_2AOhVnFNal-fjV6gYvRY4Ui7F4lNgko-nE6AcUvRX1jzWnkApokg177lAOxHX4Ws2vksj-Lq3Lx3ZPjpgfm8WrLZGwbDNtkfyoCHEV80lNfdQ7Pz0kXR4oJxYcy9Z1oxyM__yPzXYNQv9rvu3qxureJqu66MIogh9qa8D2X25n2nGWWHuqDXSLsPNNmikPtBolnXEmXeyQ7P_mzpkVHFXn-ABvXXk5kILLR2xTATSzmTmizjFuNS62Vxpjw",
            'content-type': "application/json"
            }

        conn.request("POST", f"/api/v1/namespaces/{namespace}/actions/{package_name}/{action_name}?blocking=true&result=true", headers=headers, body=params)
        response = conn.getresponse()
    except:
        # If any error occurs
        print("Network exception occurred")
    json_data = json.loads(response.readline())
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


def get_dealer(json_data):
    return CarDealer(
        int(json_data['id']),
        json_data['city'],
        json_data['state'],
        json_data['st'],
        json_data['address'],
        json_data['zip'],
        float(json_data['lat']),
        float(json_data['long']),
        json_data['short_name'],
        json_data['full_name'])

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(params):
    result = get_request('dealership-package', 'get-dealership', params)
    return map(get_dealer, result['dealerships'])


def get_dealer_review(json_data):
    if 'id' in json_data:
        review_id = int(json_data['id'])
    else:
        review_id = -1
    purchase = bool(json_data['purchase'])
    if (purchase):
        return DealerReview(
            review_id,
            json_data['name'],
            json_data['dealership'],
            json_data['review'],
            purchase,
            datetime.strptime(json_data['purchase_date'], '%m/%d/%Y'),
            json_data['car_make'],
            json_data['car_model'],
            int(json_data['car_year'])
            )
    else:
        return DealerReview(
            review_id,
            json_data['name'],
            json_data['dealership'],
            json_data['review'],
            purchase,
            None,
            None,
            None,
            None
            )

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_review_by_id_from_cf(dealer_id):
    result = get_request('review-package', 'get-review', {})
    return map(get_dealer_review, result['reviews'])

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative


