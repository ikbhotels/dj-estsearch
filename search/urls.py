from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from . import views

app_name = 'search'
urlpatterns = [
    url(r'^(?P<setid>[^/]+)$', views.index, name='index'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
