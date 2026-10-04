from django.contrib import admin
from .models import Address, Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "full_name", "phone_number", "created_at", "updated_at")
    search_fields = ("user__username", "user__email", "full_name", "phone_number")
    ordering = ("-created_at",)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "street_address", "city", "postal_code", "country", "is_default", "updated_at")
    list_filter = ("is_default", "country")
    search_fields = ("user__username", "street_address", "city", "postal_code")
    ordering = ("-is_default", "-created_at")
