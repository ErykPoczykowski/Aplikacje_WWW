from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.shortcuts import get_object_or_404
from .models import Event
from .serializers import EventModelSerializer, EventListSerializer


# --- PODEJŚCIE 1: Klasa bazowa APIView ---
class EventListAPIView(APIView):
    """
    Ręczna obsługa metod GET i POST wewnątrz klasy APIView.
    """
    def get(self, request):
        events = Event.objects.filter(is_published=True).select_related('category', 'organizer').prefetch_related('tags')
        serializer = EventListSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = EventModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# --- PODEJŚCIE 2: Widoki generyczne (generics.*) ---
class EventListCreateGenericView(generics.ListCreateAPIView):
    """
    Automatycznie implementuje GET (lista) oraz POST (tworzenie).
    Metoda get_serializer_class pozwala użyć lżejszego serializatora dla GET!
    """
    queryset = Event.objects.select_related('category', 'organizer').prefetch_related('tags').all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return EventListSerializer
        return EventModelSerializer


class EventRetrieveUpdateDestroyGenericView(generics.RetrieveUpdateDestroyAPIView):
    """
    Automatycznie implementuje GET (szczegóły), PUT, PATCH (edycja) oraz DELETE (usuwanie).
    """
    queryset = Event.objects.select_related('category', 'organizer').prefetch_related('tags').all()
    serializer_class = EventModelSerializer