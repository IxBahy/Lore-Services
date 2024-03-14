from rest_framework import serializers
from utils.models import User
from utils.serializer import UserSerializer


class StudentSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name','img_url']



