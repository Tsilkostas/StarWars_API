from rest_framework.routers import DefaultRouter
from .views import CharacterViewSet, FilmViewSet, StarshipViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register("characters", CharacterViewSet) # /api/characters/
router.register("films", FilmViewSet) # /api/films/
router.register("starships", StarshipViewSet) # /api/starships/

# The API URLs are now determined automatically by the router.
urlpatterns = router.urls