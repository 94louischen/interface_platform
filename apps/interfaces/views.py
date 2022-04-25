# Create your views here.
import os
from datetime import datetime

from django.conf import settings
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from configures.models import Configures
from envs.models import Envs
from interfaces.models import Interfaces
from interfaces.serializers import InterfaceModelSerializer, InterfaceTestCaseModelSerializers, \
    InterfaceConfiguresSerializers, InterfaceRunSerializer
from testcases.models import Testcases
from utils import common
from utils.my_mixins import RunModelMixin


class InterfacesView(RunModelMixin, viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Interfaces.objects.all()
    serializer_class = InterfaceModelSerializer
    ordering = ['create_time']

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        for result in response.data.get("results"):
            result["testcases"] = Testcases.objects.filter(interface=result.get("id")).count()
            result["configures"] = Configures.objects.filter(interface=result.get("id")).count()
        return response

    @action(methods=["GET"], detail=True, url_path="testcases")
    def testcases(self, request, *args, **kwargs):
        resp = super().retrieve(request, *args, **kwargs)
        resp.data = resp.data.pop("testcases")
        return resp

    @action(methods=["GET"], detail=True, url_path="configs")
    def configures(self, request, *args, **kwargs):
        resp = super().retrieve(request, *args, **kwargs)
        resp.data = resp.data.pop("configures")
        return resp

    @action(methods=['post'], detail=True)
    def run(self, request, *args, **kwargs):
        (instance, testcase_dir_path, env) = super().run(request, *args, **kwargs)
        [common.generate_testcase_file(testcase_obj, env, testcase_dir_path) for testcase_obj in Testcases.objects.filter(interface=instance)]
        return common.run_testcase(instance, testcase_dir_path)

    def get_serializer_class(self):
        if self.action == "testcases":
            return InterfaceTestCaseModelSerializers
        elif self.action == "configures":
            return InterfaceConfiguresSerializers
        elif self.action == "run":
            return InterfaceRunSerializer
        else:
            return super().get_serializer_class()
