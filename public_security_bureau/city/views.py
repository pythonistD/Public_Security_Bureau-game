from django.shortcuts import render
from django.contrib.auth.models import User
from .business_logic import additional_data_for_new_sybil_record
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from .serializers import AnalystSerializer, SybilSerializer
from .models import Analyst, Sybil


class AnalystViewSet(ModelViewSet):
    queryset = Analyst.objects.all()
    serializer_class = AnalystSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(fk_user=self.request.user)


class GetUsersAnalysts(ListAPIView):
    serializer_class = AnalystSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Analyst.objects.filter(fk_user_id=self.request.user)


class GetAnalystSybilList(ListAPIView):
    queryset = Sybil.objects.all()
    serializer_class = SybilSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'fk_analyst_id'

    def get_queryset(self):
        return Sybil.objects.filter(fk_analyst_id=self.kwargs[self.lookup_field])


class CreateAnalystSybil(CreateAPIView):
    queryset = Sybil.objects.all()
    serializer_class = SybilSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=additional_data_for_new_sybil_record(request.data), partial='partial')
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
