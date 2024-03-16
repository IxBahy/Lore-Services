
from rest_framework import serializers
from django.conf.global_settings import AUTH_USER_MODEL as User


class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name','img_url']
