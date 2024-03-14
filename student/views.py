
# Create your views here.
# from django.shortcuts import render
from rest_framework import mixins,generics,status
from rest_framework.response import Response
from student.serializer import *
from utils.models import  User
from rest_framework.views import APIView

class StudentsView(mixins.UpdateModelMixin,generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = StudentSerializer

    def get(self, request, *args, **kwargs):
      user_id = self.kwargs.get("id")
      self.queryset=User.objects.get(id=user_id)
      serializer = self.get_serializer(self.queryset, many=False)
      print(request.user,request.auth)
      return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        self.serializer_class = StudentSerializer
        return self.create(request, *args, **kwargs)




class StudentClubsView(mixins.CreateModelMixin,
                  generics.GenericAPIView):
    pass


class StudentProgressView():
    pass


class StudentCompletedView():
    pass


class StudentFriendsView():
    pass