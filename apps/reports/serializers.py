import re
from rest_framework import serializers

from interfaces.models import Interfaces
from projects.models import Projects
from reports.models import Reports


# def validate_include(value):
#     obj = re.match(r'^\[\d+(, *\d+)*\]$', value)
#     if obj is None:
#         raise serializers.ValidationError("参数错误")
#     result = obj.group()
#     try:
#         data = eval(result)
#     except Exception:
#         raise serializers.ValidationError("参数错误")
#     for interface_id in data:
#         if not Interfaces.objects.filter(pk=interface_id).exists():
#             raise serializers.ValidationError(f"接口id={interface_id}不存在")


class CommonSerializers(serializers.ModelSerializer):
    class Meta:
        model = Reports
        exclude = ["update_time"]
        extra_kwargs = {
            'create_time': {
                'read_only': True,
                'format': '%Y-%m-%d %H:%M:%S'
            }
        }


class ReportsSerializer(CommonSerializers):
    CommonSerializers.Meta.exclude = ["update_time"]

    # def to_representation(self, instance):
    #     ret = super().to_representation(instance)
    #     if ret.get("result"):
    #         ret["result"] = "Pass"
    #     else:
    #         ret["result"] = "Fail"
    #     return ret
