
from rest_framework import serializers
from models import Club
class ClubSerializer(serializers.ModelSerializer):
    owner_id=serializers.StringRelatedField()
    class Meta:
        model = Club
        fields = ['id', 'name', 'description', 'type', 'img_url', 'current_capacity','max_capacity','owner_id','rating']