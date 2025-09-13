from rest_framework.test import APITestCase
from unittest.mock import patch, Mock
import api.swapi_client as swapi_client
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
from .models import Character, Film, Starship

class SwapiClientTests(APITestCase):
	"""
	Tests for the SWAPI client utility functions.
	Includes tests for fetching all resources and parsing SWAPI IDs.
	"""
	@patch('api.swapi_client.requests.get')
	def test_fetch_all_success(self, mock_get):
		"""
		Test fetch_all returns all paginated results from SWAPI.
		"""
    
		# Mock paginated response
		mock_resp1 = Mock()
		mock_resp1.json.return_value = {
			"results": [{"name": "Luke"}],
			"next": "https://swapi.info/api/people/?page=2"
		}
		mock_resp1.raise_for_status.return_value = None
		mock_resp2 = Mock()
		mock_resp2.json.return_value = {
			"results": [{"name": "Leia"}],
			"next": None
		}
		mock_resp2.raise_for_status.return_value = None
		mock_get.side_effect = [mock_resp1, mock_resp2]
		results = swapi_client.fetch_all("people")
		self.assertEqual(len(results), 2)
		self.assertEqual(results[0]["name"], "Luke")
		self.assertEqual(results[1]["name"], "Leia")

	@patch('api.swapi_client.requests.get')
	def test_fetch_all_http_error(self, mock_get):
		"""
		Test fetch_all raises an exception on HTTP error.
		"""
		mock_resp = Mock()
		mock_resp.raise_for_status.side_effect = Exception("HTTP error")
		mock_get.return_value = mock_resp
		with self.assertRaises(Exception):
			swapi_client.fetch_all("people")

	def test_parse_swapi_id_valid(self):
		"""
		Test parse_swapi_id returns correct ID for a valid SWAPI URL.
		"""
		url = "https://swapi.dev/api/people/42/"
		swapi_id = swapi_client.parse_swapi_id(url)
		self.assertEqual(swapi_id, 42)

	def test_parse_swapi_id_invalid(self):
		"""
		Test parse_swapi_id returns -1 for an invalid URL.
		"""
		url = "not-a-valid-url"
		swapi_id = swapi_client.parse_swapi_id(url)
		self.assertEqual(swapi_id, -1)

class CharacterAPITests(APITestCase):
	"""
	API tests for Character endpoints: CRUD, voting, listing, and fetching from SWAPI.
	"""
	def setUp(self):
     	# Create a sample character for use in tests
		self.character = Character.objects.create(name="Luke Skywalker", swapi_id=1)
		self.character_data = {
			"name": "Han Solo",
			"swapi_id": 2,
			"height": "180",
			"mass": "80",
			"gender": "male",
			"url": "https://swapi.dev/api/people/2/"
		}
	def test_retrieve_character(self):
		"""Test retrieving a character by ID."""
		url = reverse('character-detail', args=[self.character.id])
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['id'], self.character.id)

	def test_create_character(self):
		"""Test creating a new character."""
		url = reverse('character-list')
		response = self.client.post(url, self.character_data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(response.data['name'], self.character_data['name'])

	def test_update_character(self):
		"""Test updating a character with PUT."""
		url = reverse('character-detail', args=[self.character.id])
		data = {"name": "Luke S."}
		response = self.client.put(url, {**self.character_data, **data}, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['name'], data['name'])

	def test_partial_update_character(self):
		"""Test partially updating a character with PATCH."""
		url = reverse('character-detail', args=[self.character.id])
		data = {"name": "Luke Updated"}
		response = self.client.patch(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['name'], data['name'])

	def test_delete_character(self):
		"""Test deleting a character."""
		url = reverse('character-detail', args=[self.character.id])
		response = self.client.delete(url)
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

	def test_vote_character(self):
		"""Test voting for a character."""
		url = reverse('character-vote', args=[self.character.id])
		response = self.client.post(url, {}, format='json')
		self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_201_CREATED])

	def test_list_characters(self):
		"""Test listing characters (paginated)."""
		url = reverse('character-list')
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertIn('results', response.data)

	@patch('api.swapi_client.fetch_all')
	def test_fetch_characters(self, mock_fetch_all):
		"""Test fetching characters from SWAPI via the custom fetch endpoint."""
		mock_fetch_all.return_value = [{"name": "Leia Organa", "url": "https://swapi.dev/api/people/2/"}]
		url = reverse('character-fetch')
		response = self.client.post(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertIn('stored', response.data)

class FilmAPITests(APITestCase):
	"""
	API tests for Film endpoints: CRUD, voting, listing, and fetching from SWAPI.
	"""
	def setUp(self):
		self.film = Film.objects.create(title="A New Hope", swapi_id=1)
		self.film_data = {
			"title": "The Empire Strikes Back",
			"swapi_id": 2,
			"episode_id": 5,
			"director": "Irvin Kershner",
			"producer": "Gary Kurtz",
			"release_date": "1980-05-21",
			"url": "https://swapi.dev/api/films/2/"
		}
	def test_retrieve_film(self):
		"""Test retrieving a film by ID."""
		url = reverse('film-detail', args=[self.film.id])
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['id'], self.film.id)

	def test_create_film(self):
		"""Test creating a new film."""
		url = reverse('film-list')
		response = self.client.post(url, self.film_data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(response.data['title'], self.film_data['title'])

	def test_update_film(self):
		"""Test updating a film with PUT."""
		url = reverse('film-detail', args=[self.film.id])
		data = {"title": "A New Hope Updated"}
		response = self.client.put(url, {**self.film_data, **data}, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['title'], data['title'])

	def test_partial_update_film(self):
		"""Test partially updating a film with PATCH."""
		url = reverse('film-detail', args=[self.film.id])
		data = {"title": "A New Hope Patched"}
		response = self.client.patch(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['title'], data['title'])

	def test_delete_film(self):
		"""Test deleting a film."""
		url = reverse('film-detail', args=[self.film.id])
		response = self.client.delete(url)
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

	def test_vote_film(self):
		"""Test voting for a film."""
		url = reverse('film-vote', args=[self.film.id])
		response = self.client.post(url, {}, format='json')
		self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_201_CREATED])

	def test_list_films(self):
		"""Test listing films (paginated)."""
		url = reverse('film-list')
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertIn('results', response.data)

	@patch('api.swapi_client.fetch_all')
	def test_fetch_films(self, mock_fetch_all):
		"""Test fetching films from SWAPI via the custom fetch endpoint."""
		mock_fetch_all.return_value = [{"title": "The Empire Strikes Back", "url": "https://swapi.dev/api/films/2/"}]
		url = reverse('film-fetch')
		response = self.client.post(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertIn('stored', response.data)
  
	def test_films_are_ordered_by_id(self):
		"""
		Test that the films returned by the API are ordered by id.
		"""
		url = reverse('film-list')
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		ids = [film['id'] for film in response.data['results']]
		self.assertEqual(ids, sorted(ids), "Films are NOT ordered by id!")

class StarshipAPITests(APITestCase):
	"""
	API tests for Starship endpoints: CRUD, voting, listing, and fetching from SWAPI.
	"""
	def setUp(self):
		self.starship = Starship.objects.create(name="X-wing", swapi_id=1)
		self.starship_data = {
			"name": "TIE Fighter",
			"swapi_id": 2,
			"model": "Twin Ion Engine",
			"manufacturer": "Sienar Fleet Systems",
			"url": "https://swapi.dev/api/starships/2/"
		}
	def test_retrieve_starship(self):
		"""Test retrieving a starship by ID."""
		url = reverse('starship-detail', args=[self.starship.id])
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['id'], self.starship.id)

	def test_create_starship(self):
		"""Test creating a new starship."""
		url = reverse('starship-list')
		response = self.client.post(url, self.starship_data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(response.data['name'], self.starship_data['name'])

	def test_update_starship(self):
		"""Test updating a starship with PUT."""
		url = reverse('starship-detail', args=[self.starship.id])
		data = {"name": "X-wing Updated"}
		response = self.client.put(url, {**self.starship_data, **data}, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['name'], data['name'])

	def test_partial_update_starship(self):
		"""Test partially updating a starship with PATCH."""
		url = reverse('starship-detail', args=[self.starship.id])
		data = {"name": "X-wing Patched"}
		response = self.client.patch(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['name'], data['name'])

	def test_delete_starship(self):
		"""Test deleting a starship."""
		url = reverse('starship-detail', args=[self.starship.id])
		response = self.client.delete(url)
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

	def test_vote_starship(self):
		"""Test voting for a starship."""
		url = reverse('starship-vote', args=[self.starship.id])
		response = self.client.post(url, {}, format='json')
		self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_201_CREATED])

	def test_list_starships(self):
		"""Test listing starships (paginated)."""
		url = reverse('starship-list')
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertIn('results', response.data)

	@patch('api.swapi_client.fetch_all')
	def test_fetch_starships(self, mock_fetch_all):
		"""Test fetching starships from SWAPI via the custom fetch endpoint."""
		mock_fetch_all.return_value = [{"name": "TIE Fighter", "url": "https://swapi.dev/api/starships/2/"}]
		url = reverse('starship-fetch')
		response = self.client.post(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertIn('stored', response.data)
