
from rest_framework import serializers
from club.models import Club,RoadmapWeek,Roadmap,ClubReview
from instructor.serializer import InstructorSerializer
from django.contrib.auth import get_user_model

User = get_user_model()
# ========================================================================
# ===========================  Sub Actions  ==============================


# ========================  End Of Sub Actions ===========================
# ========================================================================

# THIS SERILIZER IS ONLY HERE SINCE I CANT EXCLUDE A FIELD FROM THE drf_spectacular @extend_schema
class RoadmapWeekSwaggerSchemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoadmapWeek
        fields = ['id', 'degree', 'title', 'description']

class RoadmapWeekSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoadmapWeek
        fields = ['id', 'degree', 'title', 'description',"roadmap_id" ]


# Roadmap
class RoadmapSerializer(serializers.ModelSerializer):
    weeks=RoadmapWeekSerializer(many=True,read_only=True)
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
        fields = ['id', 'name', 'description', 'type', 'img_url','owner',"current_capacity"]


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