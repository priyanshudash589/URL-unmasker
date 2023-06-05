from rest_framework import serializers
from .models import UnsafeURL


class UnsafeURLSerializer(serializers.ModelSerializer):

    class Meta:
        model = UnsafeURL
        fields = ['id','short_url','origianl_url','status']
