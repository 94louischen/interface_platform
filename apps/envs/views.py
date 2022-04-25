from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from envs.models import Envs
from envs.serializers import EnvsModelSerializer, EnvsNameModelSerializer


class EnvsView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Envs.objects.all()
    serializer_class = EnvsModelSerializer
    ordering = ['create_time']

    @action(methods=["GET"], detail=False, url_path="names")
    def names(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def filter_queryset(self, queryset):
        if self.action == "names":
            return queryset
        else:
            return super().filter_queryset(queryset)

    def paginate_queryset(self, queryset):
        if self.action == "names":
            return None
        else:
            return super().paginate_queryset(queryset)

    def get_serializer_class(self):
        if self.action == "names":
            return EnvsNameModelSerializer
        else:
            return super().get_serializer_class()
