# from django.shortcuts import render
from rest_framework import mixins,generics,status,filters
from rest_framework.response import Response
from club.serializer import GetClubSerializer,PostClubSerializer
from club.models import Club
from rest_framework.views import APIView
# ========================================================================
# ========================   Filter Functions  ===========================
def filter_clubs(request,queryset):
    print("hereeeeeeeeeez")
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
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    pass