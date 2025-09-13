from django.db import models

class Film(models.Model):
    """
    Represents a Star Wars film.
    Stores SWAPI ID, title, episode number, director, producer, release date, SWAPI URL, and vote count.
    """
    swapi_id = models.IntegerField(unique=True)  # Unique identifier from SWAPI
    title = models.CharField(max_length=200)  # Title of the film
    episode_id = models.IntegerField(null=True, blank=True)  # Episode number (can be null)
    director = models.CharField(max_length=100, blank=True)  # Director's name
    producer = models.CharField(max_length=200, blank=True)  # Producer(s) name(s)
    release_date = models.CharField(max_length=20, blank=True)  # Release date as string
    url = models.URLField(blank=True)  # SWAPI URL for this film
    votes = models.IntegerField(default=0)  # Number of votes this film has received
    def __str__(self):
        """
        Returns the string representation of the film (its title).
        """
        return self.title
    
    
class Starship(models.Model):
    """
    Represents a Star Wars starship.
    Stores SWAPI ID, name, model, manufacturer, SWAPI URL, and vote count.
    """
    swapi_id = models.IntegerField(unique=True) # Unique identifier from SWAPI
    name = models.CharField(max_length=200) # Name of the starship
    model = models.CharField(max_length=200, blank=True) # Model of the starship
    manufacturer = models.CharField(max_length=200, blank=True) # Manufacturer of the starship
    url = models.URLField(blank=True) # SWAPI URL for this starship
    votes = models.IntegerField(default=0) # Number of votes this starship has received

    def __str__(self):
        """
        Returns the string representation of the starship (its name).
        """
        return self.name   
    
    
class Character(models.Model):
    """
    Represents a Star Wars character.
    Stores SWAPI ID, name, physical attributes, SWAPI URL, related films and starships, and vote count.
    """
    swapi_id = models.IntegerField(unique=True) # Unique identifier from SWAPI
    name = models.CharField(max_length=200) # Character's name
    height = models.CharField(max_length=50, blank=True) # Height as string (can be blank)
    mass = models.CharField(max_length=50, blank=True) # Mass as string (can be blank)
    gender = models.CharField(max_length=50, blank=True) # Gender (can be blank)
    url = models.URLField(blank=True) # SWAPI URL for this character
    films = models.ManyToManyField(Film, related_name="characters", blank=True) # Films this character appears in (many-to-many)
    starships = models.ManyToManyField(Starship, related_name="pilots", blank=True) # Starships this character can pilot (many-to-many)
    votes = models.IntegerField(default=0) # Number of votes this character has received

    def __str__(self):
        """
        Returns the string representation of the character (their name).
        """
        return self.name     
