# Auto-generates the 5 doctor URLs from DoctorViewSet.

from rest_framework.routers import DefaultRouter

from doctors.views import DoctorViewSet

router = DefaultRouter()
router.register("", DoctorViewSet, basename="doctor")

urlpatterns = router.urls
