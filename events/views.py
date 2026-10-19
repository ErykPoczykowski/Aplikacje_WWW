from django.shortcuts import render, get_object_or_404
from .models import Event, Category


def event_list(request):
    """Widok listy opublikowanych wydarzeń."""
    events = Event.objects.filter(is_published=True).select_related('category', 'organizer')
    categories = Category.objects.all()

    # Obsługa wyszukiwarki (Zadanie 3)
    q = request.GET.get('q', '')
    if q:
        events = events.filter(title__icontains=q)

    return render(request, 'events/event_list.html', {
        'events': events,
        'categories': categories,
        'q': q  # Przekazanie zapytania do szablonu
    })


def events_by_category(request, category_slug):
    """Wydarzenia przefiltrowane według kategorii."""
    category = get_object_or_404(Category, slug=category_slug)
    events = category.events.filter(is_published=True).select_related('organizer')
    categories = Category.objects.all()  # Pobranie wszystkich kategorii

    return render(request, 'events/event_list.html', {
        'events': events,
        'categories': categories,  # Przekazanie do kontekstu
        'current_category': category
    })


def event_detail(request, slug):
    """Widok pojedynczego wydarzenia na podstawie parametru slug."""
    event = get_object_or_404(
        Event.objects.select_related('category', 'organizer'),
        slug=slug,
        is_published=True
    )

    # Pobieranie podobnych wydarzeń (Zadanie 4)
    related_events = Event.objects.filter(
        category=event.category,
        is_published=True
    ).exclude(id=event.id)[:3]

    return render(request, 'events/event_detail.html', {
        'event': event,
        'related_events': related_events  # Przekazanie do szablonu
    })turn render(request, 'events/event_detail.html', {'event': event})