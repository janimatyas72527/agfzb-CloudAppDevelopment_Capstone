import json
import http.client
from datetime import datetime
from .models import CarDealer, DealerReview

def to_query_param(item):
    return f'{item[0]}={item[1]}'

def to_query_params(params):
    return '&'.join(map(to_query_param, params.items()))

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
            'authorization': "Bearer eyJraWQiOiIyMDIzMDUxMTA4MzEiLCJhbGciOiJSUzI1NiJ9.eyJpYW1faWQiOiJJQk1pZC0zMTAwMDBBUDVYIiwiaWQiOiJJQk1pZC0zMTAwMDBBUDVYIiwicmVhbG1pZCI6IklCTWlkIiwianRpIjoiYWJiZmQ4YjItMDcyZC00ZTJlLThkOWMtM2VmMTcxOTEwYTBlIiwiaWRlbnRpZmllciI6IjMxMDAwMEFQNVgiLCJnaXZlbl9uYW1lIjoiTWF0eWFzIiwiZmFtaWx5X25hbWUiOiJKYW5pIiwibmFtZSI6Ik1hdHlhcyBKYW5pIiwiZW1haWwiOiJqYW5pLm1hdHlhc0BnbWFpbC5jb20iLCJzdWIiOiJqYW5pLm1hdHlhc0BnbWFpbC5jb20iLCJhdXRobiI6eyJzdWIiOiJqYW5pLm1hdHlhc0BnbWFpbC5jb20iLCJpYW1faWQiOiJJQk1pZC0zMTAwMDBBUDVYIiwibmFtZSI6Ik1hdHlhcyBKYW5pIiwiZ2l2ZW5fbmFtZSI6Ik1hdHlhcyIsImZhbWlseV9uYW1lIjoiSmFuaSIsImVtYWlsIjoiamFuaS5tYXR5YXNAZ21haWwuY29tIn0sImFjY291bnQiOnsidmFsaWQiOnRydWUsImJzcyI6IjVhMzk1ODJkNWE4NjRjYzM5YjYzYzMwY2VlMDU2YmZjIiwiaW1zX3VzZXJfaWQiOiIxMDgxMDQzMyIsImltcyI6IjI2MzI3NTUifSwiaWF0IjoxNjg2MzE5NzczLCJleHAiOjE2ODYzMjMzNzMsImlzcyI6Imh0dHBzOi8vaWFtLmNsb3VkLmlibS5jb20vaWRlbnRpdHkiLCJncmFudF90eXBlIjoidXJuOmlibTpwYXJhbXM6b2F1dGg6Z3JhbnQtdHlwZTpwYXNzY29kZSIsInNjb3BlIjoiaWJtIG9wZW5pZCIsImNsaWVudF9pZCI6ImJ4IiwiYWNyIjoxLCJhbXIiOlsicHdkIl19.beEz2w3iOXcBwkdql-VAETMqbYq7WRPBP0BnTx94F5IcQVzR3mpyms0GQKJYObp9xjHIS1OGDLf3mSUZfm7xN_ERYZk7Qm7W0e5g8xmZw5Ah0C4RLILrKohAJ-y7_EZwTPJNk2QS1-DLNlvjgsn9_FEoUr3WoKpoAlAsrYvZuBITjL_jQdieBrKK22h4_u5ZhxJaG9TgYe1FdCeX2KXZx50-YMdWxAt3YdnDFo8ckSL8zynheyAx3S_Tcpq9TI-9Qf7ZyFOhbEXA8XtmllBkzXX1uUnbtLj9k63CFJf-mgBwELlqATdHfrQVAX0dHM7QBr498EhEVM0VsBsfEs-6OQ",
            'content-type': "application/json"
            }

        query_params = { 'blocking': 'true', 'result': 'true' }

        body = json.dumps(params, indent=4)

        conn.request("POST", f"/api/v1/namespaces/{namespace}/actions/{package_name}/{action_name}?{to_query_params(query_params)}", headers=headers, body=body)
        response = conn.getresponse()
    except:
        # If any error occurs
        print("Network exception occurred")
    json_data = json.loads(response.readline())
    return json_data


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
    result = get_request('review-package', 'get-review', {'dealership': dealer_id})
    return map(get_dealer_review, result['reviews'])

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative


