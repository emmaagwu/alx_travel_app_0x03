from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Listing, Booking, Payment, Review, Message

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ("id", "username", "email", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_superuser", "is_active")
    search_fields = ("username", "email", "role")
    ordering = ("id",)

    fieldsets = BaseUserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("phone_number", "role",)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Additional Info", {"fields": ("phone_number", "role",)}),
    )

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "host", "location", "price_per_night", "created_at")
    search_fields = ("name", "location", "host__username")
    list_filter = ("location", "created_at")

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "listing", "user", "start_date", "end_date", "status", "total_price")
    list_filter = ("status", "start_date", "end_date")
    search_fields = ("listing__name", "user__username")

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "booking", "amount", "payment_method", "payment_date")
    list_filter = ("payment_method", "payment_date")
    search_fields = ("booking__id",)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "listing", "user", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("listing__name", "user__username")

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "sender", "recipient", "sent_at")
    search_fields = ("sender__username", "recipient__username")
    list_filter = ("sent_at",)
