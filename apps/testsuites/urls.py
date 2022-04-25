from rest_framework import routers
from . import views

router = routers.SimpleRouter()  # 创建路由

router.register(r'testsuits', views.TestSuitesView)  # 注册路由

urlpatterns = router.urls   # 生成路由