from rest_framework import serializers

from configures.serializers import ConfiguresModelSerializer
from interfaces.models import Interfaces
from projects.models import Projects
from testcases.serializers import TestCasesModelSerializer


class CommonSerializers(serializers.ModelSerializer):
    class Meta:
        model = Interfaces
        exclude = ["update_time"]  # 指定排除的字段
        extra_kwargs = {
            'create_time': {
                'read_only': True,
                'format': '%Y-%m-%d %H:%M:%S'
            }
        }


class InterfaceModelSerializer(CommonSerializers):
    project = serializers.SlugRelatedField(slug_field="name", read_only=True, label="项目名称", help_text="项目名称")
    project_id = serializers.PrimaryKeyRelatedField(queryset=Projects.objects.all(), label="项目id", help_text="项目id")

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


class InterfaceModelSerializer1(serializers.ModelSerializer):

    class Meta:
        model = Interfaces
        fields = ["id", "name"]


class InterfaceTestCaseModelSerializers(CommonSerializers):
    testcases = TestCasesModelSerializer(many=True, label="所属接口用例列表", help_text="所属接口用例列表")


class InterfaceConfiguresSerializers(CommonSerializers):
    configures = ConfiguresModelSerializer(many=True, label="所属接口配置列表", help_text="所属接口配置列表")


class InterfaceRunSerializer(serializers.ModelSerializer):
    env_id = serializers.IntegerField(validators=[])

    class Meta:
        model = Interfaces
        fields = ('id', 'env_id')
