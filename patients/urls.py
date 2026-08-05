# Auto-generates the 5 patient URLs (list, create, view-one, update, delete)
# from PatientViewSet - no need to write each URL out by hand.

from rest_framework.routers import DefaultRouter

from patients.views import PatientViewSet

router = DefaultRouter()
router.register("", PatientViewSet, basename="patient")

urlpatterns = router.urls
