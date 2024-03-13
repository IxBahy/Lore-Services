
from rest_framework import serializers
from club.models import Club,RoadmapWeek,Roadmap,ClubReview
from utils.models import User
from instructor.serializer import InstructorSerializer
# ========================================================================
# ===========================  Sub Actions  ==============================


# ========================  End Of Sub Actions ===========================
# ========================================================================

class RoadmapWeekSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoadmapWeek
        fields = ['id', 'week_number', 'degree', 'title', 'description',"roadmap_id" ]


# Roadmap
class RoadmapSerializer(serializers.ModelSerializer):
    weeks=RoadmapWeekSerializer( many=True,read_only=True)
    class Meta:
        model = Roadmap
        fields = ['id', 'weeks_count', 'weeks_capacity', 'weeks' ]


class PostRoadmapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roadmap
        fields = ['id', 'weeks_capacity','weeks_count','club']


# Club members
class MembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

#  ALl Clubs
class GetClubSerializer(serializers.ModelSerializer):
    owner=serializers.StringRelatedField()

    class Meta:
        model = Club
        fields = ['id', 'name', 'description', 'type', 'img_url','owner']


# Single club
class GetClubDetailsSerializer(serializers.ModelSerializer):
    owner=InstructorSerializer()
    roadmap=RoadmapSerializer()
    class Meta:
        model = Club
        fields = ['id', 'name', 'roadmap', 'description', 'type', 'img_url', 'current_capacity','max_capacity','owner','rating']
class PostClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ['id', 'name',  'description', 'type', 'img_url', 'current_capacity','max_capacity','owner','rating']


class ClubReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClubReview
        fields = '__all__'