# Create your views here.
# from django.shortcuts import render
import json
from rest_framework import mixins, generics, status
from rest_framework.response import Response
from student.serializer import *
from club.serializer import *
from utils.serializer import UserShortSerializer
from club.models import UserRoadmapWeek
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework.decorators import api_view
from rest_framework.response import Response


User = get_user_model()


class StudentClubsView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            if request.query_params.get("student_id"):
                user = User.objects.get(id=request.query_params["student_id"])
            clubs = user.clubs.all()
            serializer = GetClubSerializer(clubs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="club_id",
            description="club id",
            required=True,
            location=OpenApiParameter.QUERY,
            type=OpenApiTypes.INT,
        ),
    ]
)
class StudentClubActionsView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:

            club_id = request.query_params["club_id"]
            user_id = request.user.id
            User.objects.get(id=user_id).clubs.add(club_id)
            return Response("club joined", status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        try:
            club_id = request.query_params["club_id"]
            user_id = request.user.id
            User.objects.get(id=user_id).clubs.remove(club_id)
            return Response("club left", status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class StudentProgressView(generics.GenericAPIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):

        try:
            user = request.user
            clubs = user.clubs.all()
            res = []
            for club in clubs:
                club_object = {
                    "name": club.name,
                    "image": club.img_url,
                }
                roadmap = club.roadmap
                weeks = roadmap.weeks.all()
                completed_weeks = UserRoadmapWeek.objects.filter(
                    user_id=user.id, week_id__in=weeks, is_completed=True
                )
                club_object["progress"] = (
                    f"{str(len(completed_weeks))}/{str(len(weeks))}"
                )
                res.append(club_object)
            return Response(res, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class StudentCompletedWeekView(generics.GenericAPIView):
    serializer_class = RoadmapWeekSerializer

    def post(self, request, week_id, *args, **kwargs):
        try:
            user = request.user
            week = RoadmapWeek.objects.get(id=week_id)
            week_status = UserRoadmapWeek.objects.filter(user_id=user, week_id=week)[0]
            if week_status.is_in_progress:
                week_status.is_completed = True
                week_status.save()
            else:
                raise Exception("Week is not in progress")
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, week_id, *args, **kwargs):
        try:
            user = request.user
            week = RoadmapWeek.objects.get(id=week_id)
            UserRoadmapWeek.objects.create(
                user_id=user, week_id=week, is_in_progress=True
            ).delete()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class StudentProgressWeekView(generics.GenericAPIView):
    serializer_class = RoadmapWeekSerializer

    def post(self, request, week_id, *args, **kwargs):
        try:
            user = request.user
            week = RoadmapWeek.objects.get(id=week_id)
            UserRoadmapWeek.objects.create(
                user_id=user, week_id=week, is_in_progress=True
            )
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, week_id, *args, **kwargs):
        try:
            user = request.user
            week = RoadmapWeek.objects.get(id=week_id)
            UserRoadmapWeek.objects.filter(
                user_id=user, week_id=week, is_in_progress=True
            ).delete()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def student_roadmap_view(request, club_id, *args, **kwargs):
    try:
        res = []
        user = request.user
        roadmap = Roadmap.objects.get(club__id=club_id)
        weeks = roadmap.weeks.all()
        for week in weeks:
            week_object = {
                "id": week.id,
                "title": week.title,
                "description": week.description,
                "degree": week.degree,
                "is_completed": UserRoadmapWeek.objects.filter(
                    user_id=user.id, week_id=week, is_completed=True
                ).exists(),
                "is_in_progress": UserRoadmapWeek.objects.filter(
                    user_id=user.id, week_id=week, is_in_progress=True
                ).exists(),
            }
            res.append(week_object)
        return Response(res, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class StudentFriendsView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            friends = user.friends.all()
            serializer = UserShortSerializer(friends, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="id",
                description="user id that will get a friend request from the current user",
                required=True,
                location=OpenApiParameter.QUERY,
                type=OpenApiTypes.INT,
            ),
        ]
    )
    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            friend_id = request.query_params["id"]
            friend = User.objects.get(id=friend_id)
            user.friends.add(friend)
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="id",
                description="user id that will be removed from the current user friends",
                required=True,
                location=OpenApiParameter.QUERY,
                type=OpenApiTypes.INT,
            ),
        ]
    )
    def delete(self, request, *args, **kwargs):
        try:
            user = request.user
            friend_id = request.query_params["id"]
            friend = User.objects.get(id=friend_id)
            user.friends.remove(friend)
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
