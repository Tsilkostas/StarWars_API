from django.contrib import admin

"""
Django admin configuration for the Star Wars API app.

Registers the Character, Film, and Starship models for management via the Django admin interface.
"""

from django.contrib import admin
from .models import Character, Film, Starship

# Register the Character model
admin.site.register(Character)

# Register the Film model
admin.site.register(Film)

# Register the Starship model
admin.site.register(Starship)
