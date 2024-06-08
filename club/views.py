# from django.shortcuts import render
from rest_framework import mixins, generics, status
from rest_framework.response import Response
from club.serializer import *
from club.models import Club, Article
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from drf_spectacular.utils import extend_schema, OpenApiParameter, inline_serializer
from drf_spectacular.types import OpenApiTypes
from rest_framework import views
from rest_framework.parsers import MultiPartParser, FormParser
import json


# ========================================================================
# ========================   Filter Functions  ===========================
def filter_clubs(request, queryset):
    name = request.query_params.get("name")
    type = request.query_params.get("type")
    rating = request.query_params.get("rating")
    category = request.query_params.get("category")
    if name:
        queryset = queryset.filter(name__icontains=name)
    if type:
        queryset = queryset.filter(type=type)
    if rating:
        queryset = queryset.filter(rating__gte=rating)
    if category:
        queryset = queryset.filter(category__icontains=category)
    return queryset


# =====================  End Of Filter Functions  ========================
# ========================================================================


# Create your views here.
class ClubsView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Club.objects.all()
    serializer_class = GetClubSerializer
    filter_fields = ["name", "type", "rating", "category"]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="name",
                description="club name",
                required=False,
                location=OpenApiParameter.QUERY,
                type=OpenApiTypes.STR,
            ),
            OpenApiParameter(
                name="type",
                description="club type",
                required=False,
                location=OpenApiParameter.QUERY,
                type=OpenApiTypes.STR,
            ),
            OpenApiParameter(
                name="rating",
                description="club rating",
                required=False,
                location=OpenApiParameter.QUERY,
                type=OpenApiTypes.INT,
            ),
            OpenApiParameter(
                name="category",
                description="club category",
                required=False,
                location=OpenApiParameter.QUERY,
                type=OpenApiTypes.STR,
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            queryset = filter_clubs(request, queryset)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except:
            return Response(
                {"error": "Request Error"}, status=status.HTTP_400_BAD_REQUEST
            )

    @extend_schema(request=PostClubSerializer)
    def post(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated]
        self.serializer_class = PostClubSerializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        club = Club.objects.get(id=serializer.data["id"]).owner = request.user
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def put(self, request, **kwargs):
        self.serializer_class = FileUploadSerializer
        self.parser_classes = (
            MultiPartParser,
            FormParser,
        )
        file = request.data["document"]
        try:
            if file:
                serializer = FileUploadSerializer(data=request.data)
                print(":::::::::::::::::::::::::::::::::::::", file)
                if serializer.is_valid():
                    serializer.save()
                    return Response("File uploaded", status=status.HTTP_201_CREATED)
                else:
                    return Response(
                        serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ClubView(mixins.UpdateModelMixin, generics.GenericAPIView):
    serializer_class = GetClubDetailsSerializer
    permission_classes = [IsAuthenticated]
    queryset = Club.objects.all()

    def get(self, request, *args, **kwargs):
        try:
            club_id = self.kwargs.get("id")
            self.queryset = Club.objects.get(id=club_id)
            serializer = self.get_serializer(self.queryset, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(request=PostClubSerializer)
    def patch(self, request, *args, **kwargs):
        self.serializer_class = PostClubSerializer
        return self.partial_update(request, *args, **kwargs)


class RoadmapView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=inline_serializer(
            name="InlinePostRoadmapSerializer",
            fields={
                "weeks": RoadmapWeekSwaggerSchemaSerializer(many=True),
                "weeks_capacity": serializers.IntegerField(),
            },
        ),
    )
    def post(self, request, id):
        weeks = request.data.get("weeks")
        roadmap_current_count = request.data.get("weeks_capacity")
        roadmap_data = {
            "weeks_capacity": 4,
            "weeks_count": roadmap_current_count,
            "club": id,
        }
        raodmap_serializer = PostRoadmapSerializer(data=roadmap_data)

        if raodmap_serializer.is_valid():
            weeks = json.loads(weeks)
            weeks = weeks["value"]
            roadmap = raodmap_serializer.save()
            for week in weeks:
                week["roadmap_id"] = roadmap.id
            weeks_serializer = RoadmapWeekSerializer(data=weeks, many=True)
            if weeks_serializer.is_valid():
                weeks_serializer.save()
                return Response("Roadmap created", status=status.HTTP_201_CREATED)
            return Response(weeks_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(raodmap_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MembersView(
    mixins.ListModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView
):
    permission_classes = [IsAuthenticated]
    serializer_class = MembersSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="name",
                description="member name",
                required=False,
                location=OpenApiParameter.QUERY,
                type=OpenApiTypes.STR,
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        try:
            club_id = self.kwargs.get("id")
            name = ""
            if request.query_params.get("name"):
                name = request.query_params.get("name")
            students = User.objects.filter(clubs__id=club_id, username__icontains=name)
            self.queryset = students
            return self.list(request, *args, **kwargs)
        except:
            return Response(
                {"error": "Request Error"}, status=status.HTTP_400_BAD_REQUEST
            )


class ReviewsView(
    mixins.ListModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView
):
    serializer_class = ClubReviewSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            club_id = self.kwargs.get("id")
            reviews = ClubReview.objects.filter(club_id=club_id)
            self.queryset = reviews
            return self.list(request, *args, **kwargs)
        except:
            return Response(
                {"error": "Request Error"}, status=status.HTTP_400_BAD_REQUEST
            )

    def post(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class ClubDocumentView(generics.GenericAPIView):
    """View to retrieve club document"""

    serializer_class = ClubDocumentSerializer

    def get(self, request, *args, **kwargs):
        try:
            club_id = self.kwargs.get("id")
            self.queryset = Article.objects.get(club_id=club_id)
            serializer = self.get_serializer(self.queryset, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ClubOwnerDetails(generics.GenericAPIView):
    serializer_class = MembersSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            club_id = self.kwargs.get("id")
            club = Club.objects.get(id=club_id)
            owner = club.owner
            self.queryset = owner
            serializer = self.get_serializer(self.queryset, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
