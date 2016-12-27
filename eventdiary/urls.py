from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from .views import home

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', home, name='home'),
    url(r'^', include('web.authentication.urls')),
    url(r'^account/', include('web.accounts.urls')),
    url(r'^center/', include('web.centers.urls')),
    # static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]
