from django.contrib.auth.models import User
from django.db import models


class Employee(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    phone = models.IntegerField()
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=50)
    place = models.CharField(max_length=200, null=True)
    department = models.CharField(max_length=200, null=True)
    designation = models.CharField(max_length=200)
    date_joined = models.DateField()

    def __str__(self):
        return self.name


class Customer(models.Model):

    # employee = models.ForeignKey(Employee, null=True, on_delete=models.SET_NULL)
    customer_name = models.CharField(max_length=200)

    customer_phone = models.IntegerField()
    customer_email = models.CharField(max_length=200, null=True)
    customer_place = models.CharField(max_length=200, null=True)
    date_visited = models.DateField()
    status = models.CharField(max_length=200, null=True)             # choices=STATUS

    def __str__(self):
        return self.customer_phone


class Menu(models.Model):
    dish_category = models.CharField(max_length=20)
    dish_name = models.CharField(max_length=20)
    dish_price = models.FloatField()

    def __str__(self):
        return self.dish_name


class Order(models.Model):

    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    menu = models.ForeignKey(Menu, null=True, on_delete=models.SET_NULL)
    customer_name_order = models.CharField(max_length=200, null=True)
    order_quantity = models.IntegerField()
    order_price = models.FloatField()
    order_date = models.DateField()

    def __str__(self):
        return self.customer_name_order


class Feedback(models.Model):

    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    menu = models.ForeignKey(Menu, null=True, on_delete=models.SET_NULL)
    customer_name_feedback = models.CharField(max_length=200, null=True)
    customer_age = models.IntegerField(null=True)
    customer_gender = models.CharField(max_length=200, null=True)      # choices=STATUS
    # rating = GenericRelation(Rating, related_query_name='foos')
    rating = models.CharField(max_length=200, null=True)         # choices=STATUS_RATING
    review = models.CharField(max_length=200, null=True)
    feedback_date = models.DateField()

    def __str__(self):
        return self.menu.dish_name


class Lead(models.Model):
    lead_name = models.CharField(max_length=200, null=True)
    lead_source = models.CharField(max_length=200, null=True)
    lead_email = models.CharField(max_length=200, null=True)
    lead_phone = models.IntegerField()
    lead_location = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.lead_name