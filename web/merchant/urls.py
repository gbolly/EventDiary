from django.conf.urls import url
from web.merchant.views import ManageCenterView


urlpatterns = [
    url(r'^centers/$', ManageCenterView.as_view(), name='merchant_manage_centers'),
]
