from django.contrib.auth.models import User
from .models import Analyst
from rest_framework.serializers import ModelSerializer


class AnalystSerializer(ModelSerializer):

    class Meta:
        model = Analyst
        fields = ['first_name', 'second_name']
