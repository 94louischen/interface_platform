from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler


class UserModelSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(min_length=6, max_length=20, write_only=True)
    token = serializers.CharField(read_only=True)

    email = serializers.EmailField(max_length=254, error_messages={"blank": "邮箱不能为空"})

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'password_confirm', 'token']
        extra_kwargs = {
            "username": {
                "min_length": 6,
                "max_length": 20,
            },
            "password": {
                "min_length": 6,
                "max_length": 20,
                "write_only": True
            }
        }

    def validate(self, attrs):
        """
        校验密码与确认密码
        :param attrs: 通过以上校验的请求体
        :return:返回校验通过的数据
        """
        if attrs["password_confirm"] != attrs["password"]:
            raise serializers.ValidationError("确认密码与密码不一致")
        return attrs

    def create(self, validated_data):
        """
        重写父类create方法，使用create_user创建用户
        :param validated_data: 校验通过的请求数据
        :return:返回模型类
        """
        validated_data.pop("password_confirm")
        instance = User.objects.create_user(**validated_data)
        # 生成token
        payload = jwt_payload_handler(instance)
        token = jwt_encode_handler(payload)
        instance.token = token
        return instance
