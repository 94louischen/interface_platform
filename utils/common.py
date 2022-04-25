import json
import os
from datetime import datetime

import yaml
# from httprunner.task import HttpRunner
# from django.conf import settings
from httprunner import HttpRunner
from rest_framework.response import Response

from django.conf import settings
from configures.models import Configures
from debugtalks.models import DebugTalks
from reports.models import Reports
from testcases.models import Testcases


def generate_testcase_file(instance, env, testcase_dir_path):
    # 定义YAML空列表
    yaml_data = {}
    # 构造默认配置参数
    yaml_data["config"] = {"name": None, "base_url": env.base_url if env else ''}
    # 获取接口和项目名称
    interface_name = instance.interface.name
    project_name = instance.interface.project.name

    # 创建以项目命名的文件夹
    testcase_dir_path = os.path.join(testcase_dir_path, project_name)
    if not os.path.exists(testcase_dir_path):
        os.makedirs(testcase_dir_path)

        # 生成debugtalk.py文件
        debugtalk_obj = DebugTalks.objects.filter(project__name=project_name).first()
        debugtalk = debugtalk_obj.debugtalk if debugtalk_obj else ''
        with open(os.path.join(testcase_dir_path, 'debugtalk.py'), 'w', encoding='utf-8') as file:
            file.write(debugtalk)

    # 创建接口目录
    testcase_dir_path = os.path.join(testcase_dir_path, interface_name)
    if not os.path.exists(testcase_dir_path):
        os.makedirs(testcase_dir_path)

    # 获取配置信息
    testcase_include = json.loads(instance.include)
    try:
        # 异常捕获一下，防止配置id不存在程序报错无法往下执行
        config_id = testcase_include.get('config')
        config_obj = Configures.objects.filter(id=config_id).first()
        if config_obj:
            config_request = json.loads(config_obj.request)
            # 添加base_url
            config_request['config']['base_url'] = env.base_url if env.base_url else ''
            # 替换全局默认的config
            # yaml_list[0] = config_request
            yaml_data["config"] = config_request["config"]
    except Exception:
        pass

    testcase_list = []  # 定义空列表
    # 获取前置用例信息并加入到YAML列表
    pre_testcase_id_list = testcase_include.get('testcases')
    for testcase_id in pre_testcase_id_list:
        try:
            testcase_request = json.loads(Testcases.objects.filter(id=testcase_id).first().request)
        except Exception:
            continue
        testcase_list.append(testcase_request)

    # 获取当前用例信息加入到YAML列表
    testcase_list.append(json.loads(instance.request))

    # 组装测试步骤
    # yaml_list.append({"teststeps": testcase_list})
    yaml_data["teststeps"] = testcase_list

    # 创建YAML文件
    testcase_dir_path = os.path.join(testcase_dir_path, 'case' + str(instance.id) + '_' + instance.name + '.yml')
    with open(testcase_dir_path, 'w', encoding='utf-8') as file:
        # yaml.dump(yaml_list, stream=file, allow_unicode=True)
        yaml.dump(yaml_data, stream=file, allow_unicode=True)


def generate_report(instance, allure_report):
    # 创建报告名称：用例名_时间戳
    report_name = instance.name + datetime.strftime(datetime.now(), '%Y%m%d%H%M%S')

    test_report = {
        'name': report_name,
        'result': True,
        'success': 1,
        'count': 1,
        'html': None,
        'summary': None,
        'report_dir': allure_report
    }
    report_obj = Reports.objects.create(**test_report)
    return report_obj.id


def cmd_run_case(dir_path, report_dir):
    """
    在终端批量执行用例
    :param dir_path:用例目录
    :param report_dir:报告目录
    :return:
    """
    allure_results = os.path.join(report_dir, 'allure-report')
    allure_report = os.path.join(report_dir, 'allure-results', datetime.strftime(datetime.now(), '%Y%m%d%H%M%S'))
    os.system(f"hrun {dir_path} --alluredir={allure_results} --clean-alluredir")
    os.system(f"allure generate {allure_results} -o {allure_report}")
    return allure_report


def run_testcase(instance, testcase_dir_path):
    try:
        allure_report = cmd_run_case(testcase_dir_path, settings.REPORT_DIR)
    except Exception:
        res = {'msg': '用例执行失败', 'code': '0'}
        return Response(res, status=400)
    report_id = generate_report(instance, allure_report)
    return Response({'id': report_id}, status=201)
