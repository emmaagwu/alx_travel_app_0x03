from rest_framework import viewsets
from .models import Listing, Booking, Payment
from .serializers import ListingSerializer, BookingSerializer
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
import requests, uuid, json


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


# ---------------------------
# Payment integration with Chapa
# ---------------------------

CHAPA_HEADERS = {
    "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}",
    "Content-Type": "application/json",
}

@csrf_exempt
def initiate_payment(request):
    if request.method == "POST":
        data = json.loads(request.body)
        booking_id = data.get("booking_id")
        email = data.get("email")

        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            return JsonResponse({"error": "Invalid booking"}, status=404)

        booking_reference = str(uuid.uuid4())[:8]
        payload = {
            "amount": str(booking.total_price),
            "currency": "ETB",
            "email": email,
            "tx_ref": booking_reference,
            "callback_url": "http://localhost:8000/api/verify-payment/",
            "return_url": "http://localhost:8000/api/payment-success/",
        }

        response = requests.post(
            f"{settings.CHAPA_BASE_URL}/transaction/initialize",
            headers=CHAPA_HEADERS,
            json=payload,
        )

        if response.status_code == 200:
            resp_data = response.json()
            checkout_url = resp_data["data"]["checkout_url"]

            Payment.objects.create(
                booking=booking,
                booking_reference=booking_reference,
                amount=booking.total_price,
                email=email,
                status="Pending",
            )

            return JsonResponse({"checkout_url": checkout_url}, status=200)

        return JsonResponse({"error": "Payment initiation failed"}, status=400)


@csrf_exempt
def verify_payment(request):
    data = json.loads(request.body)
    tx_ref = data.get("tx_ref")

    try:
        payment = Payment.objects.get(booking_reference=tx_ref)
    except Payment.DoesNotExist:
        return JsonResponse({"error": "Invalid reference"}, status=404)

    response = requests.get(
        f"{settings.CHAPA_BASE_URL}/transaction/verify/{tx_ref}",
        headers=CHAPA_HEADERS,
    )

    if response.status_code == 200:
        resp_data = response.json()
        status = resp_data["data"]["status"]

        if status == "success":
            payment.status = "Completed"
            payment.transaction_id = resp_data["data"]["transaction_id"]
            payment.save()
            # trigger Celery email task here
            return JsonResponse({"message": "Payment successful"}, status=200)
        else:
            payment.status = "Failed"
            payment.save()
            return JsonResponse({"message": "Payment failed"}, status=400)

    return JsonResponse({"error": "Verification failed"}, status=400)