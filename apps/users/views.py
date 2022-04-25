from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from users.serializers import UserModelSerializer


class UserViews(ModelViewSet):
    queryset = User.objects.all()  # 用户模型类对象
    serializer_class = UserModelSerializer  # 用户序列化器类
    ordering = ['create_time']

    @action(methods=['POST'], detail=False)
    def register(self, request, *args, **kwargs):
        """
        注册
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return self.create(request, *args, **kwargs)

    @action(methods=['GET'], detail=True)
    def check_email(self, request, email):
        """
        检查邮箱
        :param request:
        :param email:
        :return:
        """
        count = self.get_queryset(email).count()
        data = {"email": email,
                "count": count}
        return Response(data)

    @action(methods=['GET'], detail=False)
    def check_username(self, request, username):
        """
        检查用户名
        :param request:
        :param username:
        :return:
        """
        count = self.get_queryset(username).count()
        data = {"username": username,
                "count": count}
        return Response(data)

    def get_queryset(self, *args):
        # 重写父类方法
        assert self.queryset is not None, (
                "'%s' should either include a `queryset` attribute, "
                "or override the `get_queryset()` method."
                % self.__class__.__name__
        )
        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            if self.action == "check_username":
                queryset = queryset.filter(username=args[0])
            elif self.action == "check_email":
                queryset = queryset.filter(email=args[0])
            else:
                queryset = queryset.all()
        return queryset


