from django.db import models
from django.utils.timezone import now
from datetime import date
from ibm_watson.natural_language_understanding_v1 import SentimentResult


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.TextField(max_length=32)
    description = models.TextField(max_length=1024)
    def __str__(self):
        return f'{self.name}'


# <HINT> Create a Car Model model `class CarModel(models.Model)
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    CMP = 'cmp'
    SED = 'sed'
    SUV = 'suv'
    WAG = 'wag'
    VAN = 'van'
    CNV = 'cnv'
    CAR_TYPE = [
        (CMP, 'Compact'),
        (SED, 'Sedan'),
        (SUV, 'SUV'),
        (WAG, 'Wagon'),
        (VAN, 'Van'),
        (CNV, 'Convertible'),
    ]
    name = models.TextField(max_length=32)
    car_type = models.CharField(max_length=3, choices=CAR_TYPE, default=CMP)
    year = models.DateField(default=date.today().year)

    def __str__(self):
        return f'{self.name}-{self.car_type}-{str(self.year)}'


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, dealer_id, city, state, state_short, address, zip_code, lat, long, short_name, full_name):
        self.dealer_id = dealer_id
        self.city = city
        self.state = state
        self.state_short = state_short
        self.address = address
        self.zip_code = zip_code
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.full_name = full_name

def sentiment_type(sentiment):
    if (sentiment != None and 'document' and sentiment & 'label' and sentiment['document']):
        return sentiment['document']['label']
    else:
        return "neutral"

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, review_id, name, dealership, review, purchase, purchase_date, car_make, car_model, car_year, sentiment ):
        self.review_id = review_id
        self.name = name
        self.dealership = dealership
        self.review = review
        self.purchase = purchase
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
        self.sentiment_type = sentiment_type(sentiment)
