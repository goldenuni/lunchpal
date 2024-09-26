from django.contrib import admin
from lunchpal.models import Restaurant, Menu


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "address",
        "cuisine",
    )
    search_fields = (
        "name",
        "address",
        "cuisine",
    )
    list_filter = ("cuisine",)


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = (
        "restaurant",
        "date",
        "votes",
        "price",
    )
    search_fields = (
        "restaurant__name",
        "date",
    )
    list_filter = (
        "date",
        "restaurant__cuisine",
    )
    ordering = ("-date",)
