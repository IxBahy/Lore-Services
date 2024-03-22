from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema
from .serializer import *
from rest_framework import mixins,generics,status
from django.contrib.auth import get_user_model

import re

# ========================================================================
# ========================   Auth Functions  ===========================
VALID_USER="valid user"
WEEK_PASSWORD="password doesn't satisfy the constrains"
EXISTING_CREDINTALS="user with either the email or usename already exist"
def validate_user_data(data):
        '''
        create a user from the values recived from the request
        and checks if the username and email fields are uniqe
        and if not it returns an error in the response
        '''
        email=data['email']
        username=data['username']

        if User.objects.filter(email=email).count()==0 or User.objects.filter(username=username).count() ==0  :
            if is_strong_password(data["password"]):
                return VALID_USER
            else:
                return WEEK_PASSWORD
        else:
            return EXISTING_CREDINTALS

def is_strong_password(password):
    '''
     Define a regular expression pattern for a strong password
     At least 8 characters long
     Contains at least one lowercase letter, one uppercase letter, one digit, and one special character
    '''
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    # Check if the password matches the pattern
    if re.match(pattern, password):
        return True
    else:
        return False

# =====================  End Of Auth Functions  ========================
# ========================================================================




User = get_user_model()


# Create your views here.



class LoginView(TokenObtainPairView):
    serializer_class = TokenSerializer
    queryset = User.objects.all()





class LogoutView(APIView):
    pass

class RegisterView(APIView):
    @extend_schema(
            request=UserSerializer
    )
    def post(self, request):
        try:
            serializer=UserSerializer(data=request.data)
            if serializer.is_valid() :
                message=validate_user_data(request.data)
                if message==VALID_USER:
                    serializer.save()
                    return Response("user created", status=status.HTTP_201_CREATED)
                else:
                    raise ValueError(message)
            else:
                raise ValueError(serializer.errors)

        except Exception as e :

            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserView(mixins.UpdateModelMixin,generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
      self.queryset=User.objects.get(id=request.user.id)
      serializer = self.get_serializer(self.queryset, many=False)
      return Response(serializer.data)

    @extend_schema(
            request=UserPatchProfileSerializer
    )
    def patch(self, request, *args, **kwargs):
        self.serializer_class = UserPatchProfileSerializer
        return self.create(request, *args, **kwargs)

