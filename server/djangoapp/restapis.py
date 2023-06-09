import json
import http.client
from datetime import datetime
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from .models import CarDealer, DealerReview

# Disabled NLU processing as on Theia it throws error (due to obsolete dependencies)

# authenticator = IAMAuthenticator('<API Key>', disable_ssl_verification=True)
# natural_language_understanding = NaturalLanguageUnderstandingV1(
#     version='2022-04-07',
#     authenticator=authenticator
# )
# natural_language_understanding.set_service_url('<NLU Service URL>')

def to_query_param(item):
    return f'{item[0]}={item[1]}'

def to_query_params(params):
    return '&'.join(map(to_query_param, params.items()))

def call_cf_action(package_name, action_name, params):
    try:
        host = 'eu-gb.functions.cloud.ibm.com'
        namespace = '4a329e9a-d171-4f4b-b90c-cbb0435b8cc8'

        conn = http.client.HTTPSConnection(host)

        headers = {
            'accept': "application/json",
            'authorization': "Bearer eyJraWQiOiIyMDIzMDUxMTA4MzEiLCJhbGciOiJSUzI1NiJ9.eyJpYW1faWQiOiJJQk1pZC0zMTAwMDBBUDVYIiwiaWQiOiJJQk1pZC0zMTAwMDBBUDVYIiwicmVhbG1pZCI6IklCTWlkIiwianRpIjoiMzViODMwOGEtMzA4Ny00ZTc1LTlmNmMtNzBkMmFjYTQ4ZTNmIiwiaWRlbnRpZmllciI6IjMxMDAwMEFQNVgiLCJnaXZlbl9uYW1lIjoiTWF0eWFzIiwiZmFtaWx5X25hbWUiOiJKYW5pIiwibmFtZSI6Ik1hdHlhcyBKYW5pIiwiZW1haWwiOiJqYW5pLm1hdHlhc0BnbWFpbC5jb20iLCJzdWIiOiJqYW5pLm1hdHlhc0BnbWFpbC5jb20iLCJhdXRobiI6eyJzdWIiOiJqYW5pLm1hdHlhc0BnbWFpbC5jb20iLCJpYW1faWQiOiJJQk1pZC0zMTAwMDBBUDVYIiwibmFtZSI6Ik1hdHlhcyBKYW5pIiwiZ2l2ZW5fbmFtZSI6Ik1hdHlhcyIsImZhbWlseV9uYW1lIjoiSmFuaSIsImVtYWlsIjoiamFuaS5tYXR5YXNAZ21haWwuY29tIn0sImFjY291bnQiOnsidmFsaWQiOnRydWUsImJzcyI6IjVhMzk1ODJkNWE4NjRjYzM5YjYzYzMwY2VlMDU2YmZjIiwiaW1zX3VzZXJfaWQiOiIxMDgxMDQzMyIsImltcyI6IjI2MzI3NTUifSwiaWF0IjoxNjg2MzQxMjczLCJleHAiOjE2ODYzNDQ4NzMsImlzcyI6Imh0dHBzOi8vaWFtLmNsb3VkLmlibS5jb20vaWRlbnRpdHkiLCJncmFudF90eXBlIjoidXJuOmlibTpwYXJhbXM6b2F1dGg6Z3JhbnQtdHlwZTpwYXNzY29kZSIsInNjb3BlIjoiaWJtIG9wZW5pZCIsImNsaWVudF9pZCI6ImJ4IiwiYWNyIjoxLCJhbXIiOlsicHdkIl19.f7gwTHdkhC11XMu9Op5LKn0IJ9dhXIxM6te57cYnK-_REwRLwPi3UKuNWVXOD69LlqB7mVc3h91rwX-2nEOPU0gvkDVqgcalAHI66ahnZXl0BLs_aJ8FTV9bkpxFYNVTYwtviEQYSAc9jeL-GUaiO9-jPK0khA2trVCL6NlmVWToxa5hEpruSClOma_rIY7-QGy_JLoI3Bf0BQ1y0hbGWddEh6Z_gW3RtyMNzlvdRQvo2wegdXq-egBfcM_c5hFPzJPO3uVQn6pBcMRuRqvKBy57-qqNqzPVZD51_umcZgc6i1jAKEBAd2u4ZY5WrFWZXnZmzEPWA3d01Q02sFaRvg",
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
def get_dealers_from_cf(params):
    result = call_cf_action('dealership-package', 'get-dealership', params)
    return map(get_dealer, result['dealerships'])


def get_dealer_review(json_data):
    if 'id' in json_data:
        review_id = int(json_data['id'])
    else:
        review_id = -1
    review = json_data['review']
    sentiment = analyze_review_sentiments(review)
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
            int(json_data['car_year']),
            sentiment
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
            None,
            sentiment
            )

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_review_by_id_from_cf(dealership_id):
    result = call_cf_action('review-package', 'get-review', {'dealership': dealership_id})
    return map(get_dealer_review, result['reviews'])

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
    # response = natural_language_understanding.analyze(text=text, \
    #     Features=Features(sentiment=SentimentOptions(targets=['United States']))).get_result()
    # return response['sentiment']
    return None

# All information (including dealership id) is within params, so we don't need anything else
def post_review(params):
    result = call_cf_action('review-package', 'post-review', params)
    return result