
from rest_framework import serializers
from club.models import Club,RoadmapWeek,Roadmap

# ========================================================================
# ===========================  Sub Actions  ==============================


# ========================  End Of Sub Actions ===========================
# ========================================================================

class RoadmapWeekSerializer(serializers.ModelSerializer):

    class Meta:
        model = RoadmapWeek
        fields = '__all__'


# Roadmap
class RoadmapSerializer(serializers.ModelSerializer):
    weeks=RoadmapWeekSerializer( many=True,read_only=True)
    class Meta:
        model = Roadmap
        fields = '__all__'

    # def to_representation(self, value):
    #     data = super().to_representation(value)
    #     weeks_serializer



class PostRoadmapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roadmap
        fields = ['id', 'name', 'roadmap', 'description', 'type', 'img_url', 'current_capacity','max_capacity','owner','rating']


#  ALl Clubs
class GetClubSerializer(serializers.ModelSerializer):
    owner=serializers.StringRelatedField()

    class Meta:
        model = Club
        fields = ['id', 'name', 'description', 'type', 'img_url','owner']


# Single club
class GetClubDetailsSerializer(serializers.ModelSerializer):
    owner=serializers.StringRelatedField()
    roadmap=RoadmapSerializer()
    class Meta:
        model = Club
        fields = ['id', 'name', 'roadmap', 'description', 'type', 'img_url', 'current_capacity','max_capacity','owner','rating']
class PostClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ['id', 'name', 'roadmap', 'description', 'type', 'img_url', 'current_capacity','max_capacity','owner','rating']


