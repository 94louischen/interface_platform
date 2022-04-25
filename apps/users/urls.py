from django.urls import path, re_path
from rest_framework_jwt.views import obtain_jwt_token

from users import views

urlpatterns = [
    path('login/', obtain_jwt_token),
    path('register/', views.UserViews.as_view({'get': 'list', 'post': 'register'})),
    re_path(r'^(?P<username>\w{6,20})/count/$', views.UserViews.as_view({'get': 'check_username'})),
    re_path(r'^(?P<email>^[A-Za-z0-9-_\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+))/count/$',
            views.UserViews.as_view({'get': 'check_email'}))
]
