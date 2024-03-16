from rest_framework import serializers
from django.conf.global_settings import AUTH_USER_MODEL as User
from utils.serializer import UserSerializer


class StudentSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name','img_url']



