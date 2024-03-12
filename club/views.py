# from django.shortcuts import render
from rest_framework import mixins,generics,status,filters
from rest_framework.response import Response
from club.serializer import *
from club.models import Club
from rest_framework.views import APIView
# ========================================================================
# ========================   Filter Functions  ===========================
def filter_clubs(request,queryset):
    name=request.query_params.get('name')
    type=request.query_params.get('type')
    rating=request.query_params.get('rating')
    category=request.query_params.get('category')
    if name:
        queryset=queryset.filter(name__icontains=name)
    if type:
        queryset=queryset.filter(type=type)
    if rating:
        queryset=queryset.filter(rating__gte=rating)
    if category:
        queryset=queryset.filter(category__icontains=category)
    return queryset

# =====================  End Of Filter Functions  ========================
# ========================================================================




# Create your views here.
class ClubsView(mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Club.objects.all()
    serializer_class = GetClubSerializer
    filter_fields = ['name','type','rating','category']
    def get(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            queryset = filter_clubs(request,queryset)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except:
            return Response({"error": "Request Error"}, status=status.HTTP_400_BAD_REQUEST)


    def post(self, request, *args, **kwargs):
        self.serializer_class = PostClubSerializer
        return self.create(request, *args, **kwargs)


class ClubView(mixins.ListModelMixin,
                mixins.UpdateModelMixin,
                  generics.GenericAPIView):
    serializer_class = GetClubDetailsSerializer
    queryset=Club.objects.all()
    def get(self, request, *args, **kwargs):
        try:
            club_id = self.kwargs.get("pk")
            self.queryset = Club.objects.filter(id=club_id)
            return self.list(request, *args, **kwargs)
        except:
            return Response({"error": "Request Error"}, status=status.HTTP_400_BAD_REQUEST)
    def patch(self, request, *args, **kwargs):
        self.serializer_class=PostClubSerializer
        return self.partial_update(request, *args, **kwargs)





class RoadmapView(mixins.CreateModelMixin,
                mixins.UpdateModelMixin,
                  generics.GenericAPIView):
    serializer_class =PostRoadmapSerializer
    queryset=Roadmap.objects.all()

    def post(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)






class MembersView(mixins.ListModelMixin,
                mixins.UpdateModelMixin,
                  generics.GenericAPIView):
    serializer_class = MembersSerializer
    def get(self, request, *args, **kwargs):
        try:
            club_id = self.kwargs.get("pk")
            students=User.objects.filter(clubs__id=club_id)
            self.queryset =students
            return self.list(request, *args, **kwargs)
        except:
            return Response({"error": "Request Error"}, status=status.HTTP_400_BAD_REQUEST)
    def post(self, request, *args, **kwargs):
        self.serializer_class=PostClubSerializer
        return self.partial_update(request, *args, **kwargs)



class ReviewsView(mixins.ListModelMixin,
                mixins.UpdateModelMixin,
                  generics.GenericAPIView):
    serializer_class = ClubReviewSerializer
    def get(self, request, *args, **kwargs):
        try:
            club_id = self.kwargs.get("pk")
            reviews=ClubReview.objects.filter(club_id=club_id)
            self.queryset =reviews
            return self.list(request, *args, **kwargs)
        except:
            return Response({"error": "Request Error"}, status=status.HTTP_400_BAD_REQUEST)
    def post(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
