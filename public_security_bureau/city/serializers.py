from django.contrib.auth.models import User
from .models import Analyst, Sybil
from rest_framework.serializers import ModelSerializer


class AnalystSerializer(ModelSerializer):

    class Meta:
        model = Analyst
        fields = ['analyst_id', 'first_name', 'second_name']


class SybilSerializer(ModelSerializer):

    class Meta:
        model = Sybil
        fields = '__all__'
