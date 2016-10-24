from django import forms
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

from .models import Booking, BookingStatus, Center


class BookingForm(forms.Form):

    def __init__(self, user, center, *arg, **kwargs):
        self.user = user
        self.center = center
        super(BookingForm, self).__init__(*arg, **kwargs)

    customer_name = forms.CharField(max_length=200, required=True, widget = forms.TextInput(attrs = {'class':'required'}))
    booking_start_date = forms.DateField()
    booking_end_date = forms.DateField()
    phone_number = forms.IntegerField()

    def save(self):
        booking = Center.objects.get(id=self.center.id)
        print booking, "0"*50
        booking.customer_name = self.cleaned_data['customer_name']
        booking.booking_start_date = self.cleaned_data['booking_start_date']
        booking.booking_end_date = self.cleaned_data['booking_end_date']
        booking.phone_number = self.cleaned_data['phone_number']
        booking.save()
        return booking


# class BookingForm(forms.ModelForm):
#     def __init__(self, session=None, user=None, *args, **kwargs):
#         self.user = user
#         self.session = session
#         super(BookingForm, self).__init__(*args, **kwargs)
#         # fields that should remain blank / not required
#         keep_blank = []
#         # set all fields except the keep_blank ones to be required, since they
#         # need to be blank=True on the model itself to allow creating Booking
#         # instances without data
#         for name, field in self.fields.items():
#             if name not in keep_blank:
#                 self.fields[name].required = True

#     def save(self, *args, **kwargs):
#         if not self.instance.pk:
#             self.instance.user = self.user
#             self.instance.session = self.session
#             status_object, created = BookingStatus.objects.get_or_create(
#                 slug=getattr(settings, 'BOOKING_STATUS_CREATED', 'pending'))
#             self.instance.booking_status = status_object
#         return super(BookingForm, self).save(*args, **kwargs)

#     class Meta:
#         model = Booking
#         fields = ('customer_name', 'booking_start_date', 'booking_end_date', 'phone_number')
