from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from .views import home

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^chaining/', include('smart_selects.urls')),
    url(r'^$', home, name='home'),
    url(r'^', include('web.authentication.urls')),
    url(r'^account/', include('web.accounts.urls')),
    url(r'^center/', include('web.centers.urls')),
    # third party apps:
    url(r'^accounts/', include('allaccess.urls')),
    url(r'^accounts/', include('allauth.urls')),
]
