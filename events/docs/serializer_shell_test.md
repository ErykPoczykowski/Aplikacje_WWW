>>> import io
>>> from events.models import Event, Category
>>> from events.serializers import EventSerializer
>>> from rest_framework.renderers import JSONRenderer
>>> from rest_framework.parsers import JSONParser
>>> 
>>> # --- TEST 1: Pomyślna serializacja obiektu Event do JSON ---
>>> event = Event.objects.first()
>>> serializer = EventSerializer(event)
>>> print("Słownik Pythona:", serializer.data)
Słownik Pythona: {'id': 1, 'title': 'urodziny bogdana', 'slug': 'urodziny-bogdana', 'category_id': 1, 'organizer_id': 1, 'description': 'dwawdawd', 'location': 'dawdwad', 'date': '2026-10-12T14:46:07Z', 'capacity': 512, 'price': '40.00', 'is_published': False, 'created_at': '2026-10-12T14:46:09.745024Z'}
>>> 
>>> json_bytes = JSONRenderer().render(serializer.data)
>>> print("JSON:", json_bytes)
JSON: b'{"id":1,"title":"urodziny bogdana","slug":"urodziny-bogdana","category_id":1,"organizer_id":1,"description":"dwawdawd","location":"dawdwad","date":"2026-10-12T14:46:07Z","capacity":512,"price":"40.00","is_published":false,"created_at":"2026-10-12T14:46:09.745024Z"}'
>>> 
>>> # --- TEST 2: Pomyślna deserializacja i utworzenie nowego obiektu ---
>>> stream = io.BytesIO(json_bytes)
>>> data = JSONParser().parse(stream)
>>> data['title'] = "Nowe Warsztaty Pythona"
>>> data['slug'] = "nowe-warsztaty-pythona"
>>> 
>>> deserializer = EventSerializer(data=data)
>>> if deserializer.is_valid():
...     print("Dane są poprawne!")
...     print("Zwalidowane dane:", deserializer.validated_data)
...     new_event = deserializer.save()
...     print(f"Utworzono wydarzenie o id={new_event.id}")
... else:
...     print("Błędy walidacji:", deserializer.errors)
... 
Dane są poprawne!
Zwalidowane dane: {'title': 'Nowe Warsztaty Pythona', 'slug': 'nowe-warsztaty-pythona', 'category': <Category: Eventy dla dzieci>, 'organizer': <User: admin>, 'description': 'dwawdawd', 'location': 'dawdwad', 'date': datetime.datetime(2026, 10, 12, 14, 46, 7, tzinfo=zoneinfo.ZoneInfo(key='UTC')), 'capacity': 512, 'price': Decimal('40.00'), 'is_published': False}
Utworzono wydarzenie o id=6
>>> # --- TEST 3: Próba deserializacji z niepoprawnymi danymi ---
>>> invalid_data = {
...     'title': '',
...     'date': 'zla-data-2026',
...     'capacity': -5
... }
>>> bad_serializer = EventSerializer(data=invalid_data)
>>> print("Czy poprawne?", bad_serializer.is_valid())
Czy poprawne? False
>>> print("Błędy:", bad_serializer.errors)
Błędy: {'title': [ErrorDetail(string='This field may not be blank.', code='blank')], 'slug': [ErrorDetail(string='This field is required.', code='required')], 'category_id': [ErrorDetail(string='This field is required.', code='required')], 'organizer_id': [ErrorDetail(string='This field is required.', code='required')], 'description': [ErrorDetail(string='This field is required.', code='required')], 'location': [ErrorDetail(string='This field is required.', code='required')], 'date': [ErrorDetail(string='Datetime has wrong format. Use one of these formats instead: YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z].', code='invalid')], 'capacity': [ErrorDetail(string='Ensure this value is greater than or equal to 1.', code='min_value')]}
>>> 