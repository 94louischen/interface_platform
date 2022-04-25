from rest_framework import routers
from . import views

router = routers.SimpleRouter()  # 创建路由

router.register(r'interfaces', views.InterfacesView)  # 注册路由

urlpatterns = router.urls  # 生成路由
