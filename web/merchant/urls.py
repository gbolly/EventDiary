from django.conf.urls import url
from web.merchant.views import ManageCenterView, booking_list_view, edit_merchant_center, booking_action


urlpatterns = [
    url(r'^(?P<username>\w+)/centers/$', ManageCenterView.as_view(), name='merchant_manage_centers'),
    url(r'^(?P<username>\w+)/bookings/$', booking_list_view, name='booking_list'),
    url(r'^(?P<username>\w+)/bookings/approved/$', booking_action, name='booking_status'),
    url(r'^(?P<username>\w+)/(?P<center_slug>\w+)/$', edit_merchant_center, name='merchant_manage_indv_center'),
]
