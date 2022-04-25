import math

from django.contrib.auth.models import User

# Create your views here.
from django.db.models import QuerySet, Count, Sum
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from configures.models import Configures
from debugtalks.models import DebugTalks
from envs.models import Envs
from interfaces.models import Interfaces
from projects.models import Projects
from reports.models import Reports
from summary.serializers import SummarySerializer
from testcases.models import Testcases
from testsuites.models import Testsuits


class SummaryView(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()  # 用户模型类对象
    serializer_class = SummarySerializer  # 首页统计序列化器类
    ordering = ['create_time']

    def list(self, request, *args, **kwargs):
        resp = super().list(request, *args, **kwargs)
        count = {}
        count['user'] = resp.data[0]
        summary = {}
        summary['projects_count'] = Projects.objects.all().count()
        summary['interfaces_count'] = Interfaces.objects.all().count()
        summary['testcases_count'] = Testcases.objects.all().count()
        summary['testsuits_count'] = Testsuits.objects.all().count()
        summary['configures_count'] = Configures.objects.all().count()
        summary['envs_count'] = Envs.objects.all().count()
        summary['debug_talks_count'] = DebugTalks.objects.all().count()
        summary['reports_count'] = Reports.objects.all().count()
        summary['success_rate'] = math.floor((Reports.objects.aggregate(success=Sum('success')).get(
            'success') / Reports.objects.aggregate(count=Sum('count')).get('count')) * 100)
        summary['fail_rate'] = 100 - summary['success_rate']
        count['statistics'] = summary
        return Response(count)

    def get_queryset(self):
        if self.action == 'list':
            assert self.queryset is not None, (
                    "'%s' should either include a `queryset` attribute, "
                    "or override the `get_queryset()` method."
                    % self.__class__.__name__
            )

            queryset = self.queryset
            if isinstance(queryset, QuerySet):
                # Ensure queryset is re-evaluated on each request.
                queryset = queryset.filter(username=self.request.user.username)
            return queryset
        else:
            return super().get_queryset()

    def filter_queryset(self, queryset):
        if self.action == "list":
            return queryset
        else:
            return super().filter_queryset(queryset)

    def paginate_queryset(self, queryset):
        if self.action == 'list':
            return None
        else:
            return super().paginate_queryset(queryset)
