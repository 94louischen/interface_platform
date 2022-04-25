from rest_framework import serializers
from envs.models import Envs


class CommonSerializers(serializers.ModelSerializer):
    class Meta:
        model = Envs
        exclude = ["update_time"]  # 指定排除的字段
        extra_kwargs = {
            'create_time': {
                'read_only': True,
                'format': '%Y-%m-%d %H:%M:%S'
            }
        }


class EnvsModelSerializer(CommonSerializers):
    pass


class EnvsNameModelSerializer(CommonSerializers):
    class Meta:  # 重写父类属性
        model = Envs
        fields = ["id", "name"]
