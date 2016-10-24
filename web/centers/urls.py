from django.conf.urls import url

from web.centers import views

urlpatterns = [
    url(r'^$', views.center_listing, name='center_listing'),
    url(r'^(?P<name>[\w\-]+)/$', views.center_detail, name='center_detail'),
    url(r'^(?P<name>[\w\-]+)/booking/$', views.booking_view, name='booking_create'),
]
