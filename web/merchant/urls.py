from django.conf.urls import url
from web.merchant.views import ManageCenterView, edit_merchant_center


urlpatterns = [
    url(r'^(?P<username>\w+)/centers/$', ManageCenterView.as_view(), name='merchant_manage_centers'),
    url(r'^(?P<username>\w+)/(?P<center_slug>\w+)/$', edit_merchant_center, name='merchant_manage_indv_center'),
]
