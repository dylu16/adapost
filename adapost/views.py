from rest_framework import viewsets
from rest_framework.response import Response
from adapost.serializers import IngrijitorSerializer, AnimalSerializer, RezervaSerializer, EvenimentSerializer
from rest_framework.decorators import action
from adapost.models import Ingrijitor, Animal, Rezerva, Eveniment


class IngrijitorViewSet(viewsets.ModelViewSet):
    serializer_class = IngrijitorSerializer
    queryset = Ingrijitor.objects.all()

    @action(detail=False, methods=['GET'])
    def angajati_activi(self, request):
        queryset = Ingrijitor.objects.filter(este_angajat=True, este_voluntar=False)
        serializer = IngrijitorSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def voluntari_activi(self, request):
        queryset = Ingrijitor.objects.filter(este_angajat=True, este_voluntar=True)
        serializer = IngrijitorSerializer(queryset, many=True)
        return Response(serializer.data)

    def filter_queryset(self, queryset):
        pk = self.request.GET.get('id')
        if pk:
            queryset = queryset.filter(pk=pk)
        return queryset


class AnimalViewSet(viewsets.ModelViewSet):
    serializer_class = AnimalSerializer
    queryset = Animal.objects.all()

    @action(detail=False, methods=['GET'])
    def animale_adoptate(self, request):
        queryset = Animal.objects.filter(este_adoptat=True)
        serializer = AnimalSerializer(queryset, many=True)
        return Response(serializer.data)


class RezervaViewSet(viewsets.ModelViewSet):
    serializer_class = RezervaSerializer
    queryset = Rezerva.objects.all()


class EvenimentViewSet(viewsets.ModelViewSet):
    serializer_class = EvenimentSerializer
    queryset = Eveniment.objects.all()
