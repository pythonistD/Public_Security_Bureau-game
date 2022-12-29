from django.contrib.auth.models import User
from .models import Analyst, Sybil
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers


class AnalystSerializer(ModelSerializer):

    class Meta:
        model = Analyst
        fields = ['analyst_id', 'first_name', 'second_name']


class SybilSerializer(ModelSerializer):

    class Meta:
        model = Sybil
        fields = '__all__'


class CitizenCreateArrSerializer(Serializer):
    analyst_id = serializers.IntegerField()
    count_of_citizen = serializers.IntegerField()
    # citizen_type = serializers.CharField(max_length=100)
