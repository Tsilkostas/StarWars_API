from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Character, Film, Starship
from .serializers import CharacterSerializer, FilmSerializer, StarshipSerializer
from . import swapi_client


class CharacterViewSet(viewsets.ModelViewSet):
    """
    API endpoint for listing, retrieving, creating, updating, and deleting Star Wars characters.

    - Supports search by name.
    - Pagination is automatically applied if enabled in Django REST Framework settings.
    - Includes custom actions:
        * fetch: Fetches all characters from SWAPI and stores them in the database.
        * vote: Increments the vote count for a character.
    """
    queryset = Character.objects.all().order_by('id')
    serializer_class = CharacterSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]
    # Pagination is handled automatically by DRF if configured in settings.py

    @action(detail=False, methods=["post"])
    def fetch(self, request):
        """
        Fetch all characters from SWAPI and store them in the database.
        Only new characters (not already present) are added.
        Returns the number of new characters stored.
        """
        data = swapi_client.fetch_all("people")
        count = 0
        for item in data:
            swapi_id = swapi_client.parse_swapi_id(item["url"])
            # Create character if not already present
            obj, created = Character.objects.get_or_create(
                swapi_id=swapi_id,
                defaults={
                    "name": item["name"],
                    "height": item.get("height", ""),
                    "mass": item.get("mass", ""),
                    "gender": item.get("gender", ""),
                    "url": item["url"],
                },
            )
            if created:
                count += 1
        return Response({"stored": count})

    @action(detail=True, methods=["post"])
    def vote(self, request, pk=None):
        """
        Increment the vote count for a character.
        Returns the updated character data.
        """
        char = get_object_or_404(Character, pk=pk)
        char.votes += 1
        char.save()
        return Response(CharacterSerializer(char).data)

class FilmViewSet(viewsets.ModelViewSet):
    """
    API endpoint for listing, retrieving, creating, updating, and deleting Star Wars films.

    - Supports search by title.
    - Pagination is automatically applied if enabled in Django REST Framework settings.
    - Includes custom actions:
        * fetch: Fetches all films from SWAPI and stores them in the database.
        * vote: Increments the vote count for a film.
    """
    queryset = Film.objects.all().order_by('id')
    serializer_class = FilmSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["title"]
    # Pagination is handled automatically by DRF if configured in settings.py

    @action(detail=False, methods=["post"])
    def fetch(self, request):
        """
        Fetch all films from SWAPI and store them in the database.
        Only new films (not already present) are added.
        Returns the number of new films stored.
        """
        data = swapi_client.fetch_all("films")
        count = 0
        for item in data:
            swapi_id = swapi_client.parse_swapi_id(item["url"])
            # Create film if not already present
            obj, created = Film.objects.get_or_create(
                swapi_id=swapi_id,
                defaults={
                    "title": item["title"],
                    "episode_id": item.get("episode_id"),
                    "director": item.get("director", ""),
                    "producer": item.get("producer", ""),
                    "release_date": item.get("release_date", ""),
                    "url": item["url"],
                },
            )
            if created:
                count += 1
        return Response({"stored": count})

    @action(detail=True, methods=["post"])
    def vote(self, request, pk=None):
        """
        Increment the vote count for a film.
        Returns the updated film data.
        """
        film = get_object_or_404(Film, pk=pk)
        film.votes += 1
        film.save()
        return Response(FilmSerializer(film).data)

class StarshipViewSet(viewsets.ModelViewSet):
    """
    API endpoint for listing, retrieving, creating, updating, and deleting Star Wars starships.

    - Supports search by name.
    - Pagination is automatically applied if enabled in Django REST Framework settings.
    - Includes custom actions:
        * fetch: Fetches all starships from SWAPI and stores them in the database.
        * vote: Increments the vote count for a starship.
    """
    queryset = Starship.objects.all().order_by('id')
    serializer_class = StarshipSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]
    # Pagination is handled automatically by DRF if configured in settings.py

    @action(detail=False, methods=["post"])
    def fetch(self, request):
        """
        Fetch all starships from SWAPI and store them in the database.
        Only new starships (not already present) are added.
        Returns the number of new starships stored.
        """
        data = swapi_client.fetch_all("starships")
        count = 0
        for item in data:
            swapi_id = swapi_client.parse_swapi_id(item["url"])
            # Create starship if not already present
            obj, created = Starship.objects.get_or_create(
                swapi_id=swapi_id,
                defaults={
                    "name": item["name"],
                    "model": item.get("model", ""),
                    "manufacturer": item.get("manufacturer", ""),
                    "url": item["url"],
                },
            )
            if created:
                count += 1
        return Response({"stored": count})

    @action(detail=True, methods=["post"])
    def vote(self, request, pk=None):
        """
        Increment the vote count for a starship.
        Returns the updated starship data.
        """
        s = get_object_or_404(Starship, pk=pk)
        s.votes += 1
        s.save()
        return Response(StarshipSerializer(s).data)


