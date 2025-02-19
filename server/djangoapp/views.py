from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from .restapis import get_dealers_from_cf, get_dealer_review_by_id_from_cf, post_review

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
def static_django_template(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/static_django_template.html', context)



# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)


# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')


# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        # Get dealers
        dealerships = get_dealers_from_cf({})
        #
        context = { 'dealership_list': dealerships }
        #
        return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id, dealer_name):
    if request.method == "GET":
        # Get reviews based on id
        reviews = get_dealer_review_by_id_from_cf(dealer_id)
        #
        context = { 'dealer_id': dealer_id, 'dealer_name': dealer_name, 'review_list': reviews }
        #
        return render(request, 'djangoapp/dealer_details.html', context)



# Create an `add_review` view to submit a review
def add_review(request, dealer_id, dealer_name):
    cars = CarModel.objects.all()
    context = { 'cars': cars, 'dealer_id': dealer_id, 'dealer_name': dealer_name }
    if request.method == "GET":
        return render(request, 'djangoapp/add_review.html', context)


# Create a `submit_review` view to submit a review
def submit_review(request, dealer_id, dealer_name):
    if request.method == "POST":
        post_review(request.body)
        return HttpResponseRedirect('djangoapp/dealer_details.html', dealer_id, dealer_name)
