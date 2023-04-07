from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("car_dealer_signup/", views.car_dealer_signup, name="CarDealerSignup"),
    path("car_dealer_login/", views.car_dealer_login, name="CarDealerLogin"),
    path("car_dealer_signout/", views.car_dealer_signout, name="signout"),
    path("add_car/", views.add_car, name="add_car"),
    path("all_cars/", views.all_cars, name="all_cars"),
    path("update_car/<int:pk>", views.update_car, name="updateCar"),
    path("customer_signup/", views.customer_signup, name="customer_signup"),
    path("customer_login/", views.customer_login, name="customer_login"),
    path("customer_homepage/", views.customer_homepage, name="customer_homepage"),
    path("search_results/", views.search_results, name="search_results"),
    path("car_rent/", views.car_rent, name="car_rent"),
    path("order_details/", views.order_details, name="order_details"),
]
