import datetime
from django import forms
from django.db import models
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import widgets

from .models import Booking, BookingStatus, Center


class BookingForm(forms.ModelForm):

    def __init__(self, user, center, *arg, **kwargs):
        self.user = user
        self.center = center
        super(BookingForm, self).__init__(*arg, **kwargs)
        self.fields['booking_start_date'].widget = widgets.AdminDateWidget()
        self.fields['booking_end_date'].widget = widgets.AdminDateWidget()

    class Meta:
        model = Booking
        fields = ['customer_name', 'booking_start_date', 'booking_end_date', 'phone_number']

class CenterForm(forms.ModelForm):
    class Meta:
        model = Center
        fields = ["price", "capacity", "name", "location", "address", "image", "description"]
