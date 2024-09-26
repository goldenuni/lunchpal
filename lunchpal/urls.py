from django.urls import path

from lunchpal.views import (
    RestaurantListCreateView,
    MenuViewSet,
    CurrentDayMenuView,
    VoteMenuView,
    CurrentDayResultView,
)

app_name = "lunchpal"

urlpatterns = [
    path(
        "restaurants/",
        RestaurantListCreateView.as_view(),
        name="restaurant-list-create",
    ),
    path(
        "menu/today/", CurrentDayMenuView.as_view(), name="current-day-menu"
    ),
    path(
        "menu/today/results/",
        CurrentDayResultView.as_view(),
        name="current-day-menu-result",
    ),
    path(
        "menu/<int:menu_id>/vote/",
        VoteMenuView.as_view(),
        name="vote-for-menu",
    ),
    path(
        "menu/",
        MenuViewSet.as_view({"get": "list", "post": "create"}),
        name="menu-list-create",
    ),
    path(
        "menu/<int:pk>/",
        MenuViewSet.as_view({"get": "retrieve"}),
        name="menu-detail",
    ),
]
