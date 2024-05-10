from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from club.serializer import GetClubSerializer
User = get_user_model()
class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):

            user = User.objects.create(
                username=validated_data['username'],
                # password=validated_data['password'], if I'll hash the password in the front first
                email=validated_data['email'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name']
            )
            user.set_password(validated_data['password'])
            user.save()
            return user
    class Meta:
        model = User
        fields = ("id",'username', 'email', 'password', 'first_name', 'last_name',)
        extra_kwargs = {'password':{'write_only':True,'required':True},"id":{'read_only':True}}



class TokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['type']=user.type
        return token


class UserPatchProfileSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = User
        fields = UserSerializer.Meta.fields + ('birth_date', 'phone', 'img_url',)

class UserProfileSerializer(UserSerializer):
    clubs=GetClubSerializer(many=True,read_only=True)
    friends=UserSerializer(many=True,read_only=True)
    class Meta(UserSerializer.Meta):
        model = User
        fields = UserSerializer.Meta.fields + ('birth_date', 'phone', 'img_url', 'type', 'clubs', 'chats',"friends",)



class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id","email", "username", "img_url", "type","first_name","last_name",)