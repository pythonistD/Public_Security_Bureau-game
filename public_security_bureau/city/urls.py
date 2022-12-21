from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import AnalystViewSet

router = SimpleRouter()
router.register(r'analyst', AnalystViewSet)


urlpatterns = router.urls
