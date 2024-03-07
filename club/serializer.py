
from rest_framework import serializers
from club.models import Club
class GetClubSerializer(serializers.ModelSerializer):
    owner=serializers.StringRelatedField()
    class Meta:
        model = Club
        fields = ['id', 'name', 'description', 'type', 'img_url','owner']
class GetClubDetailsSerializer(serializers.ModelSerializer):
    owner=serializers.StringRelatedField()
    class Meta:
        model = Club
        fields = ['id', 'name', 'description', 'type', 'img_url', 'current_capacity','max_capacity','owner','rating']
class PostClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ['id', 'name', 'description', 'type', 'img_url', 'current_capacity','max_capacity','owner','rating']