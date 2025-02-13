from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import TypeDepense, Depense
from .serializers import TypeDepenseSerializer, DepenseSerializer

# CRUD pour TypeDepense
@api_view(['GET', 'POST'])
def type_depense_list(request):
    if request.method == 'GET':
        types = TypeDepense.objects.all()
        serializer = TypeDepenseSerializer(types, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TypeDepenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def type_depense_detail(request, pk):
    try:
        type_depense = TypeDepense.objects.get(pk=pk)
    except TypeDepense.DoesNotExist:
        return Response({'error': 'TypeDepense not found'}, status=status.HTTP_404_NOT_FOUND)

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


# CRUD pour Depense
@api_view(['GET', 'POST'])
def depense_list(request):
    if request.method == 'GET':
        depenses = Depense.objects.all()
        serializer = DepenseSerializer(depenses, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        print(request.data)
        serializer = DepenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def depense_detail(request, pk):
    try:
        depense = Depense.objects.get(pk=pk)
    except Depense.DoesNotExist:
        return Response({'error': 'Depense not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DepenseSerializer(depense)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = DepenseSerializer(depense, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        depense.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
