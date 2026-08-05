# The master map of every URL in the project. Each line below either points
# straight to a view, or hands off to one app's own urls.py for anything
# starting with that prefix (e.g. everything under /api/patients/ is decided
# by patients/urls.py).

from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    # Visiting the bare site, or just /api/, sends you to the interactive docs
    # instead of a blank "not found" page.
    path("", RedirectView.as_view(url="/api/docs/", permanent=False)),
    path("api/", RedirectView.as_view(url="/api/docs/", permanent=False)),
    path("admin/", admin.site.urls),  # Django's built-in admin dashboard
    path("api/auth/", include("accounts.urls")),
    path("api/patients/", include("patients.urls")),
    path("api/doctors/", include("doctors.urls")),
    path("api/mappings/", include("mappings.urls")),
    # Raw API description, and the interactive docs page built from it.
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
]
