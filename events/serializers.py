from rest_framework import serializers
from django.utils import timezone
from .models import Category, Tag, Event


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']
        read_only_fields = ['id']


class CategorySerializer(serializers.ModelSerializer):
    events_count = serializers.IntegerField(source='events.count', read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'events_count', 'created_at']
        read_only_fields = ['id', 'created_at', 'events_count']


class EventListSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    organizer_username = serializers.ReadOnlyField(source='organizer.username')
    is_free = serializers.SerializerMethodField()
    short_description = serializers.SerializerMethodField()
    tags_count = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'slug', 'category_name', 'organizer_username',
            'date', 'location', 'price', 'is_free', 'short_description', 'tags_count'
        ]

    def get_is_free(self, obj) -> bool:
        return obj.price == 0

    def get_short_description(self, obj) -> str:
        if len(obj.description) > 80:
            return obj.description[:80] + "..."
        return obj.description

    def get_tags_count(self, obj) -> int:
        """Zwraca liczbę tagów przypisanych do wydarzenia."""
        return obj.tags.count()



class EventModelSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    organizer_username = serializers.ReadOnlyField(source='organizer.username')

    tags_details = TagSerializer(source='tags', many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        source='tags',
        write_only=True,
        required=False
    )

    is_free = serializers.SerializerMethodField()
    days_until_event = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'slug', 'category', 'category_name',
            'organizer', 'organizer_username', 'tags_details', 'tag_ids',
            'description', 'location', 'date', 'capacity', 'price',
            'is_free', 'days_until_event', 'is_published',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_is_free(self, obj) -> bool:
        return obj.price == 0

    def get_days_until_event(self, obj) -> int:
        delta = obj.date - timezone.now()
        return max(0, delta.days)

    def validate_date(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError("Termin wydarzenia musi być datą w przyszłości!")
        return value

    def validate_capacity(self, value):
        if value < 5:
            raise serializers.ValidationError("Minimalna liczba uczestników wydarzenia wynosi 5 osób.")
        return value

    def validate(self, attrs):
        # Pobieranie wartości ze słownika attrs
        title = attrs.get('title', getattr(self.instance, 'title', ''))
        price = attrs.get('price', getattr(self.instance, 'price', 0))
        is_published = attrs.get('is_published', getattr(self.instance, 'is_published', True))
        description = attrs.get('description', getattr(self.instance, 'description', ''))
        location = attrs.get('location', getattr(self.instance, 'location', ''))
        capacity = attrs.get('capacity', getattr(self.instance, 'capacity', 0))

        if any(word in title.lower() for word in ['darmow', 'bezpłatn', 'free']) and price > 0:
            raise serializers.ValidationError({
                "price": "Wydarzenie oznaczone w tytule jako bezpłatne nie może mieć ceny wyższej niż 0.00 PLN."
            })

        if is_published and len(description.strip()) < 20:
            raise serializers.ValidationError({
                "description": "Opublikowane wydarzenie musi posiadać szczegółowy opis (minimum 20 znaków)."
            })

        is_url_location = location.startswith(('http://', 'https://'))
        combined_text = f"{title} {description}".lower()

        if any(word in combined_text for word in ['online', 'webinar']) and not is_url_location:
            raise serializers.ValidationError({
                "location": "Dla wydarzeń online pole lokalizacji musi zawierać poprawny adres URL (http:// lub https://)."
            })

        if not is_url_location and capacity > 1000:
            raise serializers.ValidationError({
                "capacity": "Maksymalna pojemność dla wydarzeń stacjonarnych nie może przekraczać 1000 osób."
            })

        return attrs