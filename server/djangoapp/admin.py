from django.contrib import admin
from .models import CarMake, CarModel


# Register your models here.

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    model = CarModel
    list_display = ('name', 'car_type', 'year')
    list_filter = ['name', 'car_type', 'year']

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    model = CarMake
    inlines = [CarModelInline]
    list_display = ['name', 'description']
    list_filter = ['name', 'description']

# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
