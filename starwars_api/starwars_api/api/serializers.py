from rest_framework import serializers
from .models import Character, Film, Starship


class FilmSerializer(serializers.ModelSerializer):
    """
    Serializer for the Film model.
    Serializes all fields of a Star Wars film, including related characters.
    """
    class Meta:
        model = Film
        fields = "__all__"

class StarshipSerializer(serializers.ModelSerializer):
    """
    Serializer for the Starship model.
    Serializes all fields of a Star Wars starship, including related pilots.
    """
    class Meta:
        model = Starship
        fields = "__all__"

class CharacterSerializer(serializers.ModelSerializer):
    """
    Serializer for the Character model.
    Serializes all fields of a Star Wars character, including related films and starships.
    """
    films = FilmSerializer(many=True, read_only=True) # Nested serialization for related films
    starships = StarshipSerializer(many=True, read_only=True) # Nested serialization for related starships

    class Meta:
        model = Character
        fields = "__all__"