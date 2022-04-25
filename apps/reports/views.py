# Create your views here.
import json
import os

from django.conf import settings
from django.http.response import StreamingHttpResponse
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from reports.models import Reports
from reports.serializers import ReportsSerializer
from reports.utils import *


class ReportsView(ListModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Reports.objects.all()
    serializer_class = ReportsSerializer
    ordering = ['create_time']

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        try:
            # response.data['summary'] = json.loads(response.data['summary'])
            os.system(f"allure open {response.data.get('report_dir')}")
        except Exception as e:
            pass
        return response

    @action(detail=True)
    def download(self, request, *args, **kwargs):
        # 获取报告源码
        instance = self.get_object()
        # 把源码写入html
        file_dir = os.path.join(settings.REPORT_DIR, instance.name + ".html")
        with open(file_dir, "w") as file:
            file.write(instance.html)
        # 通过生成器方式返回文件流
        response = StreamingHttpResponse(read_file(file_dir))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = f"attachment; filename*=UTF-8''{instance.name}"
        return response
