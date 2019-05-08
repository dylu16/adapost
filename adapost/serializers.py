from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from adapost.models import Ingrijitor, Animal, Rezerva, Eveniment


class IngrijitorSerializer(ModelSerializer):
    class Meta:
        model = Ingrijitor
        fields = '__all__'


class AnimalSerializer(ModelSerializer):
    sex = serializers.CharField(source='get_sex_display')
    talie = serializers.CharField(source='get_talie_display')
    specie = serializers.CharField(source='get_specie_display')
    varsta = serializers.CharField(read_only=True)

    class Meta:
        model = Animal
        fields = ('id', 'nume', 'specie', 'luna', 'anul', 'sex', 'talie', 'observatie', 'este_adoptat', 'varsta')

    def get_varsta(self, obj):
        return obj.varsta


class RezervaSerializer(ModelSerializer):
    dimensiune = serializers.CharField(source='get_dimensiune_display')

    class Meta:
        model = Rezerva
        fields = ('id', 'numar', 'animal', 'dimensiune', 'observatii')
        depth = 1


class EvenimentSerializer(ModelSerializer):
    ingrijitor = IngrijitorSerializer(many=False)
    rezerva = RezervaSerializer(many=False)

    class Meta:
        model = Eveniment
        fields = '__all__'
        depth = 1
