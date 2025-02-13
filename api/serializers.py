from rest_framework import serializers
from .models import TypeDepense, Depense

class TypeDepenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeDepense
        fields = '__all__'


class DepenseSerializer(serializers.ModelSerializer):
    # type_depense = TypeDepenseSerializer()

    class Meta:
        model = Depense
        fields = '__all__'
