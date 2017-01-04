from django.conf.urls import url

from web.centers import views

urlpatterns = [
    url(r'^$', views.CenterListView.as_view(), name='center_listing'),
    url(r'^new/$', views.new_center, name='new_center'),
    url(r'^edit-center/(?P<slug>[\w\-]+)/$', views.edit_center, name='edit-center'),
    url(r'^(?P<slug>[\w\-]+)/$', views.center_detail, name='center_detail'),
    url(r'^(?P<slug>[\w\-]+)/booking/$', views.booking_view, name='booking_create'),
]
