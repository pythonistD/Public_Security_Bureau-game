from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .serializers import AnalystSerializer
from .models import Analyst


class AnalystViewSet(ModelViewSet):
    queryset = Analyst.objects.all()
    serializer_class = AnalystSerializer
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        serializer.save(fk_user=self.request.user)

