import os
from datetime import datetime

from django.conf import settings

from envs.models import Envs


class RunModelMixin:

    def run(self, request, *args, **kwargs):
        # 获取模型类对象
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        # 获取系统配置模型类对象
        env = Envs.objects.get(id=serializer.validated_data.get('env_id'))
        # 创建以时间戳命名的文件夹
        testcase_dir_path = os.path.join(settings.SUITS_DIR, datetime.strftime(datetime.now(), '%Y%m%d%H%M%S'))
        os.mkdir(testcase_dir_path)
        return instance, testcase_dir_path, env
