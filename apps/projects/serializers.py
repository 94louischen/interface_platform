import copy

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from interfaces.serializers import InterfaceModelSerializer, InterfaceModelSerializer1
from projects.models import Projects


class CommonModelSerializer(serializers.ModelSerializer):
    """
    公共序列化器类
    """
    name = serializers.CharField(label='项目名称', help_text='项目名称', min_length=1, max_length=8,
                                 validators=[UniqueValidator(Projects.objects.all(), message='项目名不能重复')])

    class Meta:
        model = Projects
        # fields = "__all__"
        exclude = ["update_time"]
        extra_kwargs = {
            'create_time': {
                'read_only': True,
                'format': '%Y-%m-%d %H:%M:%S'
            }
        }


class ProjectModelSerializer(CommonModelSerializer):
    """
    项目列表
    """
    pass


# class ProjectInterfaceModelSerializer(CommonModelSerializer):
#     """
#     项目所属接口
#     """
#     interfaces = InterfaceModelSerializer(read_only=True, many=True)

# 2021/2/18调整
class ProjectInterfaceModelSerializer(serializers.ModelSerializer):
    """
    项目所属接口
    """
    interfaces = InterfaceModelSerializer1(read_only=True, many=True)

    class Meta:
        model = Projects
        fields = ['interfaces']


class ProjectsNameSerializer(CommonModelSerializer):
    """
    项目名称列表
    """

    class Meta:
        model = Projects
        fields = ['id', 'name']


class ProjectRunSerializer(CommonModelSerializer):
    """
    系统环境
    """
    env_id = serializers.IntegerField(validators=[])

    class Meta:
        model = Projects
        fields = ('id', 'env_id')
