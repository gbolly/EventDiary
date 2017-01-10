import datetime
from django import forms
from django.db import models
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import widgets
from cloudinary.forms import CloudinaryJsFileField, CloudinaryUnsignedJsFileField

from .models import Booking, BookingStatus, Center, CenterPhoto


class BookingForm(forms.ModelForm):

    def __init__(self, user, center, *arg, **kwargs):
        self.user = user
        self.center = center
        super(BookingForm, self).__init__(*arg, **kwargs)
        self.fields['booking_start_date'].widget = widgets.AdminDateWidget()
        self.fields['booking_end_date'].widget = widgets.AdminDateWidget()

    class Meta:
        model = Booking
        fields = ['customer_name', 'customer_email', 'phone_number', 'booking_start_date', 'booking_end_date']

class CenterForm(forms.ModelForm):
    class Meta:
        model = Center
        fields = ["name", "price", "capacity", "address", "state", "lga", "description"]

class ImageForm(forms.ModelForm):    
    class Meta:
        model = CenterPhoto
        fields = ['image']
