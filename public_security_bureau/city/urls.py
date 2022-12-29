from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import AnalystViewSet, GetUsersAnalysts, GetAnalystSybilList, CreateAnalystSybil,\
    CreateNumberOfCitizens

router = SimpleRouter()
router.register(r'analyst', AnalystViewSet)

urlpatterns = [
    path('analyst/my/', GetUsersAnalysts.as_view()),
    path('sybil/<int:fk_analyst_id>/', GetAnalystSybilList.as_view()),
    path('sybil/', CreateAnalystSybil.as_view()),
    path('citizen-n/', CreateNumberOfCitizens.as_view())
]
urlpatterns += router.urls

