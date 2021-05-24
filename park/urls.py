from django.urls import path
from authentication.views import LoginView
from park.views import (
    UserView,
    LevelsView,
    PricingView,
    VehicleView,
    VehiclePaymentView,
)


urlpatterns = [
    path("login/", LoginView.as_view()),
    path("accounts/", UserView.as_view()),
    path("levels/", LevelsView.as_view()),
    path("pricings/", PricingView.as_view()),
    path("vehicles/", VehicleView.as_view()),
    path("vehicles/<int:vehicle_id>", VehiclePaymentView.as_view()),
]
