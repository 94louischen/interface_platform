import os
from datetime import datetime

from django.conf import settings
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from envs.models import Envs
from interfaces.models import Interfaces
from testcases.models import Testcases
from testsuites.models import Testsuits
from testsuites.serializers import TestSuitesSerializer, TestSuitesDetailSerializer, TestSuitesCreateSerializer, \
    TestSuiteRunSerializer
from utils import common
from utils.my_mixins import RunModelMixin


class TestSuitesView(RunModelMixin, viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Testsuits.objects.all()
    serializer_class = TestSuitesSerializer
    ordering = ['create_time']

    @action(methods=['post'], detail=True)
    def run(self, request, *args, **kwargs):
        (instance, testcase_dir_path, env) = super().run(request, *args, **kwargs)
        [common.generate_testcase_file(testcase_obj, env, testcase_dir_path) for interface_id in eval(instance.include)
         for testcase_obj in Testcases.objects.filter(interface_id=interface_id)]
        return common.run_testcase(instance, testcase_dir_path)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TestSuitesDetailSerializer
        elif self.action == 'create':
            return TestSuitesCreateSerializer
        elif self.action == 'run':
            return TestSuiteRunSerializer
        else:
            return super().get_serializer_class()
