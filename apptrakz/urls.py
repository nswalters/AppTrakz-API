from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
# from rest_framework import routers

from apptrakzapi.models import *
from apptrakzapi.views import *

# router = routers.DefaultRouter(trailing_slash=False)

urlpatterns = [
    url(r'^register$', register_user),
    url(r'^login$', login_user),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
