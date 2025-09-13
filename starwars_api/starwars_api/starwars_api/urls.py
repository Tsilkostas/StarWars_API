"""
URL configuration for starwars_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
"""
URL configuration for the starwars_api project.

This file defines the root URL patterns for the project, including:
- Django admin interface
- API endpoints (characters, films, starships)
- API schema and interactive documentation (Swagger UI and Redoc)
"""

from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls), # Django admin interface
    path("api/", include("api.urls")), # Main API endpoints
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'), # OpenAPI schema
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'), # Swagger UI docs
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'), # Redoc docs
]
