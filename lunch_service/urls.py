from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/user/",
        include("user.urls", namespace="user"),
    ),
    path("api/lunchpal/", include("lunchpal.urls", namespace="lunchpal")),
]
