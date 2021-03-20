from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from rest_framework import routers

from apptrakzapi.models import *
from apptrakzapi.views import *

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'user', UserView, 'user')
router.register(r'companies', CompanyView, 'company')
router.register(r'jobs', JobView, 'job')
router.register(r'applications', ApplicationView, 'application')
router.register(r'statuses', StatusView, 'status')
router.register(r'job_contacts', JobContactView, 'job_contact')
router.register(r'company_notes', CompanyNoteView, 'company_note')
router.register(r'job_notes', JobNoteView, 'job_note')
router.register(r'contact_notes', ContactNoteView, 'contact_note')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^register$', register_user),
    url(r'^login$', login_user),
    url(r'^sankey$', sankey),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
