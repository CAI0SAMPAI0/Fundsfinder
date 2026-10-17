from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(url="/api/v1/fundos", permanent=False)),
    path("admin/", admin.site.urls),
    path("api/v1/", include("api.urls", namespace="api")),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]