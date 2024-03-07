from django.shortcuts import render
from rest_framework import mixins
from rest_framework import generics
from models import Club

# Create your views here.
class ClubView(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Club.objects.all()
    # serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)