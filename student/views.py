
# Create your views here.
# from django.shortcuts import render
from rest_framework import mixins,generics,status
from rest_framework.response import Response
from student.serializer import *
from utils.models import  User
from utils.serializer import  UserShortSerializer
from club.models import UserRoadmapWeek
# from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes


User=get_user_model()



@extend_schema(
        parameters=[
            OpenApiParameter(name="club_id", description="club id", required=True,location=OpenApiParameter.QUERY, type=OpenApiTypes.INT),
        ]

)
class StudentClubsView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]


    def post(self, request, *args, **kwargs):
        try:

            club_id=request.query_params['club_id']
            user_id=request.user.id
            User.objects.get(id=user_id).clubs.add(club_id)
            return Response("club joined", status=status.HTTP_201_CREATED)

        except Exception as e :
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, *args, **kwargs):
        try:
            club_id=request.data['club_id']
            user_id=request.user.id
            User.objects.get(id=user_id).clubs.remove(club_id)
            return Response("club left", status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class StudentProgressView(generics.GenericAPIView):

    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):

        try:
            user=request.user
            clubs=user.clubs.all()
            res=[]
            for club in clubs:
                club_object={"name":club.name,"image":club.img_url,}
                roadmap=club.roadmap
                weeks=roadmap.weeks.all()
                completed_weeks=UserRoadmapWeek.objects.filter(user_id=user.id,week_id__in=weeks,is_completed=True)
                club_object["progress"]=f'{str(len(completed_weeks))}/{str(len(weeks))}'
                res.append(club_object)
            return Response(res, status=status.HTTP_200_OK)

        except Exception as e :
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
        parameters=[
            OpenApiParameter(name="club_id", description="club id", required=True,location=OpenApiParameter.QUERY, type=OpenApiTypes.INT),
            OpenApiParameter(name="week_number", description="week number", required=True,location=OpenApiParameter.QUERY, type=OpenApiTypes.INT),
        ]

)
class StudentCompletedWeekView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            user=request.user
            club_id=request.query_params['club_id']
            week_number=request.query_params['week_number']
            club=user.clubs.get(id=club_id)
            roadmap=club.roadmap
            week=roadmap.weeks.get(degree=week_number)
            UserRoadmapWeek.objects.create(user_id=user,week_id=week,is_completed=True)
            return Response(status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, *args, **kwargs):
        try:
            user=request.user
            club_id=request.query_params['club_id']
            week_number=request.query_params['week_number']
            club=user.clubs.get(id=club_id)
            roadmap=club.roadmap
            week=roadmap.weeks.get(degree=week_number)
            UserRoadmapWeek.objects.filter(user_id=user,week_id=week,is_completed=True).delete()
            return Response(status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class StudentFriendsView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        try:
            user=request.user
            friends=user.friends.all()
            serializer = UserShortSerializer(friends, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[
            OpenApiParameter(name="id", description="user id that will get a friend request from the current user", required=True,location=OpenApiParameter.QUERY, type=OpenApiTypes.INT),
        ]

)
    def post(self, request, *args, **kwargs):
        try:
            user=request.user
            friend_id=request.query_params['id']
            friend=User.objects.get(id=friend_id)
            user.friends.add(friend)
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e :
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    @extend_schema(
        parameters=[
            OpenApiParameter(name="id", description="user id that will be removed from the current user friends", required=True,location=OpenApiParameter.QUERY, type=OpenApiTypes.INT),
        ]

)
    def delete(self, request, *args, **kwargs):
        try:
            user=request.user
            friend_id=request.query_params['id']
            friend=User.objects.get(id=friend_id)
            user.friends.remove(friend)
            return Response(status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)