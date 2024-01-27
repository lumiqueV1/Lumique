# Beautyswipe/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Define urlpatterns before using +=
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # Include Django authentication URLs
    path('', include('Beautyswipe_v1.urls', namespace='Beautyswipe_v1')),
]

# Use += to add static/media URL patterns
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)