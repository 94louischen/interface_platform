import re
from rest_framework import serializers

from interfaces.models import Interfaces
from projects.models import Projects
from testsuites.models import Testsuits


def validate_include(value):
    obj = re.match(r'^\[\d+(, *\d+)*\]$', value)
    if obj is None:
        raise serializers.ValidationError("参数错误")
    result = obj.group()
    try:
        data = eval(result)
    except Exception:
        raise serializers.ValidationError("参数错误")
    for interface_id in data:
        if not Interfaces.objects.filter(pk=interface_id).exists():
            raise serializers.ValidationError(f"接口id={interface_id}不存在")


class CommonSerializers(serializers.ModelSerializer):
    project = serializers.SlugRelatedField(slug_field="name", read_only=True, label="项目名称", help_text="项目名称")
    project_id = serializers.PrimaryKeyRelatedField(read_only=True, label="项目id", help_text="项目id")

    class Meta:
        model = Testsuits
        exclude = ["update_time"]
        extra_kwargs = {
            'create_time': {
                'read_only': True,
                'format': '%Y-%m-%d %H:%M:%S'
            },
            'update_time': {
                'read_only': True,
                'format': '%Y-%m-%d %H:%M:%S'
            }
        }


class TestSuitesSerializer(CommonSerializers):
    CommonSerializers.Meta.exclude = ["include"]


class TestSuitesDetailSerializer(CommonSerializers):
    CommonSerializers.Meta.exclude = ["id", "create_time", "update_time"]


class TestSuitesCreateSerializer(CommonSerializers):
    project_id = serializers.PrimaryKeyRelatedField(label="项目id", help_text="项目id", queryset=Projects.objects.all())
    CommonSerializers.Meta.exclude = []
    read_only_fields = ["id", "project", "create_time", "update_time"]
    CommonSerializers.Meta.extra_kwargs['include'] = {'validators': [validate_include], 'write_only': True}

    def to_internal_value(self, data):
        """
        修改反序列后的部分值
        :param data:
        :return:
        """
        data = super().to_internal_value(data)
        if data.get("project_id", 0):  # 这个是为了partial_update接口没传project_id做的一个异常捕获
            data["project_id"] = data.get("project_id").id
        return data


class TestSuiteRunSerializer(serializers.ModelSerializer):
    env_id = serializers.IntegerField(validators=[])

    class Meta:
        model = Testsuits
        fields = ('id', 'env_id')
