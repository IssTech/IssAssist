# Django Core Modules
from rest_framework import serializers

# Apps specific
from core.models import CoreConfig
from isssys.models import IssSys

class CoreConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoreConfig
        fields = '__all__'

class IssSysSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssSys
        fields = '__all__'
