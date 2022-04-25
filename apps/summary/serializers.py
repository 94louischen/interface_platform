from rest_framework import serializers
from django.contrib.auth.models import User


class SummarySerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'date_joined', 'last_login', 'is_superuser']
        extra_kwargs = {
            'date_joined': {
                'format': '%Y-%m-%d %H:%M:%S'
            }
        }