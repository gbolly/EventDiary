from django.conf.urls import url

# from .views import RegistrationView
from django.contrib.auth import views
from .views import register

urlpatterns = [
    url(r'^$', register, name='register'),
]
