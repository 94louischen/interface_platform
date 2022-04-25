from rest_framework import serializers
from debugtalks.models import DebugTalks


class CommonModelSerializer(serializers.ModelSerializer):
    project = serializers.SlugRelatedField(slug_field="name", read_only=True, label="项目名称", help_text="项目名称")

    class Meta:
        model = DebugTalks
        fields = ["id", "name", "project"]


class DebugTalksSerializer(CommonModelSerializer):
    pass


class DebugTalksDetailSerializer(CommonModelSerializer):
    class Meta:
        model = DebugTalks
        fields = ["id", "debugtalk"]


class DebugTalksUpdateSerializer(CommonModelSerializer):
    class Meta:
        model = DebugTalks
        fields = ["id", "debugtalk", "name", "project"]
        extra_kwargs = {"debugtalk": {"write_only": True}, "name": {"read_only": True}}


class DebugTalksCreateSerializer(serializers.ModelSerializer):
    # project = serializers.SlugRelatedField(slug_field="name", read_only=True, label="项目名称", help_text="项目名称")

    class Meta:
        model = DebugTalks
        fields = ["debugtalk", "name", "project"]
