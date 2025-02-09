from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.parsers import MultiPartParser, FormParser
from .models import CustomUser, TypeDepense, Depense
from .serializers import (UserRegistrationSerializer,UserLoginSerializer,CustomUserSerializer, TypeDepenseSerializer,DepenseSerializer, )
from rest_framework import serializers, viewsets, permissions


@api_view(['POST'])
def register(request):
    """Créer un nouveau compte utilisateur"""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': CustomUserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    """Authentifier un utilisateur et générer un token"""
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = authenticate(email=serializer.validated_data['email'], password=serializer.validated_data['password'])

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': CustomUserSerializer(user).data,
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }, status=status.HTTP_200_OK)

        return Response({'error': 'Email ou mot de passe incorrect'}, status=status.HTTP_401_UNAUTHORIZED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_users(request):
    """Récupérer la liste des utilisateurs"""
    users = CustomUser.objects.all()
    serializer = CustomUserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """Déconnecter un utilisateur en invalidant son token"""
    try:
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({'error': 'Token de rafraîchissement manquant'}, status=status.HTTP_400_BAD_REQUEST)

        token = RefreshToken(refresh_token)
        token.blacklist()

        return Response({'message': 'Déconnexion réussie'}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    


# Viewset pour type de Depense

# class TypeDepenseViewSet(viewsets.ModelViewSet):
#     queryset = TypeDepense.objects.all()
#     serializer_class = TypeDepenseSerializer
#     permission_classes = [permissions.IsAuthenticated]

# API pour TypeDepense
@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def type_depense(request):
    if request.method == 'GET':
        types_depenses = TypeDepense.objects.all()
        serializer = TypeDepenseSerializer(types_depenses, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = TypeDepenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def type_depense_detail(request, pk):
    try:
        type_depense = TypeDepense.objects.get(pk=pk)
    except TypeDepense.DoesNotExist:
        return Response({'error': 'Type de dépense non trouvé'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = TypeDepenseSerializer(type_depense)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = TypeDepenseSerializer(type_depense, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        type_depense.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# viewSet pour Depense
# class DepenseViewSet(viewsets.ViewSet):
#     queryset = Depense.objects.all()
#     serializer_class = DepenseSerializer
#     permission_classes = [permissions.IsAuthenticated]
#     parser_classes = [MultiPartParser, FormParser]


#     def perform_create(self, serializer):
#         type_depense = serializer.validated_data["type_depense"]
#         serializer.save(user=self.request.user, type_depense=type_depense)

# API pour Depense
@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def depense(request):
    if request.method == 'GET':
        depenses = Depense.objects.all()
        serializer = DepenseSerializer(depenses, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = DepenseSerializer(data=request.data)
        if serializer.is_valid():
            type_depense = serializer.validated_data.get("type_depense")
            serializer.save(user=request.user, type_depense=type_depense)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def depense_detail(request, pk):
    try:
        depense = Depense.objects.get(pk=pk)
    except Depense.DoesNotExist:
        return Response({'error': 'Dépense non trouvée'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = DepenseSerializer(depense)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = DepenseSerializer(depense, data=request.data)
        if serializer.is_valid():
            type_depense = serializer.validated_data.get("type_depense")
            serializer.save(user=request.user, type_depense=type_depense)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        depense.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)