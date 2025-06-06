
from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = "__all__"
        read_only_fields = ["is_deleted","deleted_at"]

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ('email',"password",'first_name','last_name')

    def validate_password(self,value:str):
        return make_password(value)


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Добавляем пользовательские данные в полезную нагрузку
        if user.is_staff:
            token['group'] = 'admin'
        else:
            token['group'] = 'user'


        return token

ALLOWED_AVATARS = ['/media/avatars/avatar-blue.svg', '/media/avatars/avatar-pink.svg', '/media/avatars/avatar-violet.svg', '/media/avatars/avatar-yellow.svg','/media/avatars/Group 1000006285.png']

class ProfileSerializer(serializers.Serializer):

    first_name = serializers.CharField(max_length=25)
    last_name = serializers.CharField(max_length=25)
    email = serializers.EmailField()
    avatar = serializers.CharField(required=False)


    def validate_avatar(self, value):
        if value not in ALLOWED_AVATARS:
            raise serializers.ValidationError(f"Недопустимый аватар {value}",)
        return value
    #
    # def update(self, instance, validated_data):
    #     avatar = validated_data.get('avatar')
    #     if avatar:
    #         instance.avatar = f"{avatar}"
    #     # Обновляем другие поля, если есть
    #     for attr, value in validated_data.items():
    #         if attr != 'avatar':
    #             setattr(instance, attr, value)
    #     instance.save()
    #     return instance


    def update(self, instance, validated_data):
        avatar = validated_data.pop('avatar', None)

        if avatar:
            instance.avatar = avatar  # ✔ avatar теперь строка — путь к svg

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance