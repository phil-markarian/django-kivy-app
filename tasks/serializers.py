## about serializers: https://www.django-rest-framework.org/api-guide/serializers/

from rest_framework import serializers
from .models import *

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'