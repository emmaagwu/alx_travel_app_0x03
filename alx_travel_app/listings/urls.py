from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListingViewSet, BookingViewSet, initiate_payment, verify_payment

router = DefaultRouter()
router.register(r"listings", ListingViewSet, basename="listing")
router.register(r"bookings", BookingViewSet, basename="booking")

urlpatterns = [
    path("api/", include(router.urls)),

    path("api/payments/initiate/", initiate_payment, name="initiate-payment"),
    path("api/payments/verify/<str:transaction_ref>/", verify_payment, name="verify-payment"),
]