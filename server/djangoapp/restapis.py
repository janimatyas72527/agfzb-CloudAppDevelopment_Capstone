import json
import http.client
from datetime import date
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
            'authorization': "<Auth Token>",
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
    return DealerReview(
        int(json_data['id']),
        json_data['name'],
        json_data['dealership'],
        json_data['review'],
        bool(json_data['purchase']),
        date.fromisoformat(json_data['purchase_date']),
        json_data['car_make'],
        json_data['car_model'],
        int(json_data['car_year'])
        )

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_review_by_id_from_cf(dealer_id):
    result = get_request('review-package', 'get-review', {'id': dealer_id})
    return map(result.reviews)

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative


