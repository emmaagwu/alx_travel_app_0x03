
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Listing, Booking, Payment, Review, Message

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'phone_number', 'role']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ListingSerializer(serializers.ModelSerializer):
    host = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Listing
        fields = ['id', 'name', 'description', 'location', 'price_per_night', 'host', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'host']


class BookingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    listing = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'listing', 'user', 'start_date', 'end_date', 'status', 'total_price', 'created_at']
        read_only_fields = ['id', 'status', 'total_price', 'created_at', 'user', 'listing']


class PaymentSerializer(serializers.ModelSerializer):
    booking = serializers.PrimaryKeyRelatedField(queryset=Booking.objects.all())

    class Meta:
        model = Payment
        fields = ['id', 'booking', 'amount', 'payment_method', 'payment_date']
        read_only_fields = ['id', 'payment_date']


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    listing = serializers.PrimaryKeyRelatedField(queryset=Listing.objects.all())

    class Meta:
        model = Review
        fields = ['id', 'listing', 'user', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'created_at', 'user']


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField(read_only=True)
    recipient = serializers.StringRelatedField()

    class Meta:
        model = Message
        fields = ['id', 'sender', 'recipient', 'content', 'sent_at']
        read_only_fields = ['id', 'sender', 'sent_at']
