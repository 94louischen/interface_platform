import json
import os
from datetime import datetime

from django.conf import settings
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from envs.models import Envs
from testcases.models import Testcases
from testcases.serializers import TestCaseModelSerializer1, TestCaseRunSerializer
from utils import handle_datas
from utils import common
from utils.my_mixins import RunModelMixin


class TestCasesView(RunModelMixin, viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Testcases.objects.all()
    serializer_class = TestCaseModelSerializer1
    search_fields = ['name']
    ordering = ['-create_time']

    def retrieve(self, request, *args, **kwargs):
        # 用例模型类对象
        testcase_obj = self.get_object()

        # 用例前置信息
        testcase_include = json.loads(testcase_obj.include)

        # 用例请求信息
        testcase_request = json.loads(testcase_obj.request)
        # testcase_request_datas = testcase_request.get('test').get('request')
        testcase_request_datas = testcase_request.get('request')

        # 处理用例的validate列表
        # testcase_validate = testcase_request.get('test').get('validate')
        testcase_validate = testcase_request.get('validate')
        testcase_validate_list = handle_datas.handle_data1(testcase_validate)

        # 处理用例的param数据
        testcase_params = testcase_request_datas.get('params')
        testcase_params_list = handle_datas.handle_data4(testcase_params)

        # 处理用例的header列表
        testcase_headers = testcase_request_datas.get('headers')
        testcase_headers_list = handle_datas.handle_data4(testcase_headers)

        # 处理用例variables变量列表
        # testcase_variables = testcase_request.get('test').get('variables')
        testcase_variables = testcase_request.get('variables')
        testcase_variables_list = handle_datas.handle_data2(testcase_variables)

        # 处理form表单数据
        testcase_form_datas = testcase_request_datas.get('data')
        testcase_form_datas_list = handle_datas.handle_data6(testcase_form_datas)

        # 处理json数据
        # testcase_json_datas = str(testcase_request_datas.get('json'))
        testcase_json_datas = json.dumps(testcase_request_datas.get('json'), ensure_ascii=False)

        # 处理extract数据
        # testcase_extract_datas = testcase_request.get('test').get('extract')
        testcase_extract_datas = testcase_request.get('extract')
        testcase_extract_datas_list = handle_datas.handle_data4(testcase_extract_datas)

        # 处理parameters数据
        # testcase_parameters_datas = testcase_request.get('test').get('parameters')
        testcase_parameters_datas = testcase_request.get('parameters')
        testcase_parameters_datas_list = handle_datas.handle_data3(testcase_parameters_datas)

        # 处理setupHooks数据
        # testcase_setup_hooks_datas = testcase_request.get('test').get('setup_hooks')
        testcase_setup_hooks_datas = testcase_request.get('setup_hooks')
        testcase_setup_hooks_datas_list = handle_datas.handle_data5(testcase_setup_hooks_datas)

        # 处理teardownHooks数据
        # testcase_teardown_hooks_datas = testcase_request.get('test').get('teardown_hooks')
        testcase_teardown_hooks_datas = testcase_request.get('teardown_hooks')
        testcase_teardown_hooks_datas_list = handle_datas.handle_data5(testcase_teardown_hooks_datas)

        datas = {
            'author': testcase_obj.author,
            'testcase_name': testcase_obj.name,
            'selected_configure_id': testcase_include.get('config'),
            'selected_interface_id': testcase_obj.interface_id,
            'selected_project_id': testcase_obj.interface.project.id,
            'selected_testcase_id': testcase_include.get('testcases'),
            'method': testcase_request_datas.get('method'),
            'url': testcase_request_datas.get('url'),
            'param': testcase_params_list,
            'header': testcase_headers_list,
            'variable': testcase_form_datas_list,
            'jsonVariable': testcase_json_datas,
            'extract': testcase_extract_datas_list,
            'validate': testcase_validate_list,
            'globalVar': testcase_variables_list,
            'parameterized': testcase_parameters_datas_list,
            'setupHooks': testcase_setup_hooks_datas_list,
            'teardownHooks': testcase_teardown_hooks_datas_list
        }
        return Response(datas)

    @action(methods=['post'], detail=True)
    def run(self, request, *args, **kwargs):
        (instance, testcase_dir_path, env) = super().run(request, *args, **kwargs)
        # 创建yaml文件
        common.generate_testcase_file(instance, env, testcase_dir_path)
        # 执行用例
        return common.run_testcase(instance, testcase_dir_path)

    def get_serializer_class(self):
        return TestCaseRunSerializer if self.action == 'run' else self.serializer_class
