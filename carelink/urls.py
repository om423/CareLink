from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path

from carelink.admin import admin_dashboard, admin_dashboard_api


def health(request):
    return JsonResponse({"status": "ok"})


def readiness(request):
    return JsonResponse({"ready": True})


# Customize admin site
admin.site.site_header = "CareLink Platform Administration"
admin.site.site_title = "CareLink Admin"
admin.site.index_title = "Welcome to CareLink Platform Administration"

urlpatterns = [
    path("admin/dashboard/", admin.site.admin_view(admin_dashboard), name="admin_dashboard"),
    path("admin/dashboard/api/", admin.site.admin_view(admin_dashboard_api), name="admin_dashboard_api"),
    path("admin/", admin.site.urls),
    path("", include("home.urls")),
    path("accounts/", include("accounts.urls")),
    path("profiles/", include("profiles.urls")),
    path("triage/", include("triage.urls")),
    path("doctors/", include("doctors.urls")),
    path("appointments/", include("appointments.urls")),
    path("healthz/", health),
    path("readyz/", readiness),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
