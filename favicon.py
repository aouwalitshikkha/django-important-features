import os
from django.views.static import serve
from django.urls import path
from django.conf import settings



path('favicon.ico', serve, {'path': 'favicon.ico', 'document_root': os.path.join(settings.BASE_DIR, '')}),
