# Django Default Modules
from django.shortcuts import render
from rest_framework import viewsets, filters, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
#from rest_framework.views import APIView

# Token Authenication Import
from rest_framework.permissions import IsAuthenticated

# Apps specific
from core.models import CoreConfig
from isssys.models import IssSys
# Serializers
from .serializers import (
    CoreConfigSerializer,
    IssSysSerializer,
    )

# Python Libraries
import json

TEST = 0

# Logging
import logging
log = logging.getLogger(__name__)

class CoreConfigViewSet(ModelViewSet):
    serializer_class = CoreConfigSerializer
    if TEST == 0:
        permission_classes = [IsAuthenticated]

        def get_queryset(self):
            queryset = CoreConfig.objects.filter(user=self.request.user)
            return queryset

        def perform_create(self, serializer):
            serializer.save(user=self.request.user)

    else:
        queryset = CoreConfig.objects.all()

class IssSysViewSet(ModelViewSet):
    serializer_class = IssSysSerializer
    #queryset = IssSys.objects.all()
    if TEST == 0:
        permission_classes = [IsAuthenticated]

        def get_queryset(self):
            queryset = IssSys.objects.filter(user=self.request.user)
            return queryset

    else:
        queryset = IssSys.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
