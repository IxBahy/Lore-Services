from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
User = get_user_model()
class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):

            user = User.objects.create(
                username=validated_data['username'],
                # password=validated_data['password'],
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
        write_only_fields = ('password',)
        read_only_fields = ('id',)


class TokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        return token