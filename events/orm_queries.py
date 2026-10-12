# events/orm_queries.py

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventhub.settings')
django.setup()

# 2. Import modelu
from events.models import Event


def run_queries():
    print("--- Rozpoczynam wykonywanie zapytań QuerySet ---\n")

    published_events = Event.objects.filter(is_published=True).order_by('date')
    print("1. Opublikowane wydarzenia (chronologicznie):")
    for event in published_events:
        print(f"   - {event.title} (Data: {event.date.strftime('%Y-%m-%d %H:%M')})")

    large_events = Event.objects.filter(capacity__gte=50)
    print("\n2. Wydarzenia na minimum 50 osób:")
    for event in large_events:
        print(f"   - {event.title} (Limit miejsc: {event.capacity})")

    free_events_count = Event.objects.filter(price=0.00).count()
    print(f"\n3. Łączna liczba darmowych wydarzeń: {free_events_count}")

    print("\n4. Zmiana statusu opublikowanego wydarzenia:")
    event_to_update = Event.objects.filter(is_published=True).first()

    if event_to_update:
        print(f"   Przed zmianą - '{event_to_update.title}' (is_published: {event_to_update.is_published})")

        event_to_update.is_published = False
        event_to_update.save()

        print(f"   Po zmianie   - Zapisano status is_published na: {event_to_update.is_published}")
    else:
        print("   Nie znaleziono żadnego opublikowanego wydarzenia w bazie.")

    print("\n--- Koniec zapytań ---")


if __name__ == "__main__":
    run_queries()