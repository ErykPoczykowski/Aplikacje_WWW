from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Category, Event
from .serializers import CategorySerializer, EventModelSerializer, EventListSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    Kompletny zestaw operacji CRUD dla kategorii wydarzeń.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def destroy(self, request, *args, **kwargs):
        """Blokada usunięcia kategorii, która posiada przypisane wydarzenia."""
        category = self.get_object()
        if category.events.exists():
            return Response(
                {"error": "Nie można usunąć kategorii, do której są przypisane wydarzenia."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)

    # Niestandardowa akcja dla konkretnej kategorii: GET /events/api/v1/categories/{id}/events/
    @action(detail=True, methods=['get'])
    def events(self, request, pk=None):
        """Zwraca opublikowane wydarzenia przypisane do danej kategorii."""
        category = self.get_object()
        events = category.events.filter(is_published=True).select_related('category', 'organizer').prefetch_related('tags')
        serializer = EventListSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EventViewSet(viewsets.ModelViewSet):
    """
    Kompletny zestaw operacji CRUD dla wydarzeń z dynamicznym wyborem serializatora
    oraz niestandardowymi akcjami biznesowymi.
    """
    queryset = Event.objects.select_related('category', 'organizer').prefetch_related('tags').all()

    def get_serializer_class(self):
        """
        Dla listy wydarzeń oraz akcji zwracających kolekcje używamy lżejszego EventListSerializer.
        Dla szczegółów (retrieve) oraz zapisu (create, update, partial_update) używamy EventModelSerializer.
        """
        if self.action in ['list', 'upcoming']:
            return EventListSerializer
        return EventModelSerializer

    # Niestandardowa akcja dla kolekcji: GET /events/api/v1/events/upcoming/
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Zwraca wyłącznie opublikowane wydarzenia, które odbędą się w przyszłości."""
        upcoming_events = self.get_queryset().filter(
            is_published=True,
            date__gte=timezone.now()
        ).order_by('date')
        serializer = self.get_serializer(upcoming_events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Niestandardowa akcja dla pojedynczego obiektu: POST /events/api/v1/events/{id}/publish_toggle/
    @action(detail=True, methods=['post'])
    def publish_toggle(self, request, pk=None):
        """Przełącza status publikacji wydarzenia (is_published)."""
        event = self.get_object()
        event.is_published = not event.is_published
        event.save(update_fields=['is_published', 'updated_at'])
        status_text = "opublikowane" if event.is_published else "ukryte"
        return Response({
            "message": f"Wydarzenie '{event.title}' zostało {status_text}.",
            "is_published": event.is_published
        }, status=status.HTTP_200_OK)