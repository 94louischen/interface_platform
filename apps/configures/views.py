import json

from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from configures.models import Configures
from configures.serializers import ConfiguresModelSerializer1
from utils import handle_datas


class ConfiguresView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Configures.objects.all()
    serializer_class = ConfiguresModelSerializer1
    ordering = ['create_time']

    def retrieve(self, request, *args, **kwargs):
        # 配置模型类
        configure_obj = self.get_object()
        # 配置请求信息
        configure_request = json.loads(configure_obj.request)
        # 配置请求头信息
        # header_datas = configure_request.get('config').get('request').get('headers')
        # variables_datas = configure_request.get('config').get('variables')
        header_datas = None
        variables_datas = None
        datas = {
            'author': configure_obj.author,
            'configure_name': configure_obj.name,
            'selected_interface_id': configure_obj.interface.id,
            'selected_project_id': configure_obj.interface.project_id,
            'header': handle_datas.handle_data4(header_datas),
            'globalVar': handle_datas.handle_data2(variables_datas)
        }
        return Response(datas)
