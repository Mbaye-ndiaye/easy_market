from rest_framework import serializers
from .models import *


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'telephone']
        extra_kwargs = {'id': {'read_only': True}}

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'telephone']


# Serialser pour type de Depense
class TypeDepenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeDepense
        fields = '__all__'



# Serialiser pour les Depenses
class DepenseSerializer(serializers.ModelSerializer):
    piece_justificative_url = serializers.SerializerMethodField()

    def get_piece_justificative_url(self, obj):
        if obj.piece_justificative:
            return obj.piece_justificative.url
        return None
    class Meta:
        model = Depense
        fields = '__all__'

