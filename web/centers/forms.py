import datetime
from django import forms
from django.db import models
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.extras.widgets import SelectDateWidget

from .models import Booking, BookingStatus, Center


class BookingForm(forms.Form):

    def __init__(self, user, center, *arg, **kwargs):
        self.user = user
        self.center = center
        super(BookingForm, self).__init__(*arg, **kwargs)

    customer_name = forms.CharField(max_length=200, required=True, widget = forms.TextInput(attrs = {'class':'required'}))
    booking_start_date = forms.DateField(widget=SelectDateWidget)
    booking_end_date = forms.DateField(widget=SelectDateWidget)
    phone_number = forms.IntegerField()

    def save(self):
        booking = Center.objects.get(id=self.center.id)
        print(dir(booking))
        booking.customer_name = self.cleaned_data['customer_name']
        booking.booking_start_date = self.cleaned_data['booking_start_date']
        booking.booking_end_date = self.cleaned_data['booking_end_date']
        booking.phone_number = self.cleaned_data['phone_number']
        booking.save()
        print booking
        return booking


# class BookingForm(forms.ModelForm):

#     def __init__(self, user, center, *arg, **kwargs):
#         self.user = user
#         self.center = center
#         super(BookingForm, self).__init__(*arg, **kwargs)

#     class Meta:
#         model = Booking
#         exclude = ()

#         def save(self, commit=True):
#             booking = super(BookingForm, self).save(commit=False)
#             print booking
#             if commit:
#                 booking.save()
#                 self.save_m2m()

class CenterForm(forms.ModelForm):
    class Meta:
        model = Center
        fields = ["price", "capacity", "description", "name", "location", "address", "image"]
