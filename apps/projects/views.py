import os
from datetime import datetime

from django.conf import settings
from django.db.models import Count
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from envs.models import Envs
from interfaces.models import Interfaces
from projects.serializers import ProjectInterfaceModelSerializer, ProjectsNameSerializer, ProjectRunSerializer
from projects.serializers import ProjectModelSerializer
from testcases.models import Testcases
from testsuites.models import Testsuits
from utils import common
from utils.my_mixins import RunModelMixin
from .models import *
from rest_framework import viewsets


class ProjectViewSet(RunModelMixin, viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Projects.objects.all()
    serializer_class = ProjectModelSerializer
    search_fields = ["project_name", 'project_manager']
    ordering = ['create_time']

    @action(methods=["GET"], detail=True)
    def interfaces(self, request, *args, **kwargs):
        # return super().retrieve(request, *args, **kwargs)
        # 2021/2/18调整
        response = super().retrieve(request, *args, **kwargs)
        response.data = response.data.get('interfaces')
        return response

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        for result in response.data.get("results"):
            result["testsuits"] = Testsuits.objects.filter(project=result.get("id")).count()
            interface_testcase_qs = Interfaces.objects.values('id').annotate(testcase=Count('testcases')).filter(
                project=result.get("id"))
            result["interfaces"] = interface_testcase_qs.count()
            testcase_count = 0
            for one_interface_testcase in interface_testcase_qs:
                testcase_count += one_interface_testcase.get('testcase')
            result["testcases"] = testcase_count

            configures_count = 0
            interface_configures_qs = Interfaces.objects.values('id').annotate(configures=Count('configures')).filter(
                project=result.get("id"))
            for one_interface_configures in interface_configures_qs:
                configures_count += one_interface_configures.get('configures')
            result["configures"] = configures_count
        return response

    @action(methods=['GET'], detail=False)
    def names(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(methods=['post'], detail=True)
    def run(self, request, *args, **kwargs):
        (instance, testcase_dir_path, env) = super().run(request, *args, **kwargs)
        [common.generate_testcase_file(testcase_obj, env, testcase_dir_path) for interface_obj in
         Interfaces.objects.filter(project=instance) for testcase_obj in
         Testcases.objects.filter(interface=interface_obj)]
        return common.run_testcase(instance, testcase_dir_path)

    def get_serializer_class(self):
        if self.action == "interfaces":
            return ProjectInterfaceModelSerializer
        elif self.action == 'names':
            return ProjectsNameSerializer
        elif self.action == 'run':
            return ProjectRunSerializer
        else:
            return self.serializer_class

    def filter_queryset(self, queryset):
        if self.action == "names":
            return queryset
        else:
            return super().filter_queryset(queryset)

    def paginate_queryset(self, queryset):
        if self.action == 'names':
            return None
        else:
            return super().paginate_queryset(queryset)
