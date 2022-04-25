from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from debugtalks.models import DebugTalks
from debugtalks.serializers import DebugTalksSerializer, DebugTalksDetailSerializer, DebugTalksUpdateSerializer, \
    DebugTalksCreateSerializer


class DebugTalksView(CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = DebugTalks.objects.all()
    serializer_class = DebugTalksSerializer
    ordering = ['create_time']

    def get_serializer_class(self):
        if self.action == "retrieve":
            return DebugTalksDetailSerializer
        elif self.action == "update":
            return DebugTalksUpdateSerializer
        elif self.action == "create":
            return DebugTalksCreateSerializer
        else:
            return super().get_serializer_class()
