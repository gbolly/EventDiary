from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View, ListView
from django.shortcuts import render, render_to_response, HttpResponseRedirect
from django.contrib.auth.models import User
from django.forms import modelformset_factory
from django_tables2 import RequestConfig
from django.core.mail import EmailMultiAlternatives
from django.template import RequestContext, Engine, loader

from web.centers.baseviews import CenterListBaseView
from web.centers.forms import CenterForm, ImageForm
from web.centers.models import Center, CenterPhoto, Booking
from web.centers.context_processor import Image_Effects
from web.merchant.tables import BookingTable

LOGIN_URL = '/login/'
EMAIL_SENDER = 'info@theeventdiary.com'

class ManageCenterView(CenterListBaseView):
    """Manage a single center"""

    def get(self, request, username):
        """Renders a page showing a center that was created by a merchant
        """

        list_title = "My Centers"
        list_description = "All centers posted by you"
        template = "center.html"

        if request.user.is_authenticated:
            if request.user.userprofile.is_merchant:
                merchant_id = request.user.id
                centers = Center.objects.filter(user_id=merchant_id)
                # get the rendered list of deals
                rendered_center_list = self.render_center_list(request, queryset=centers, title=list_title, description=list_description, username=request.user)
                context = {
                    'rendered_center_list': rendered_center_list,
                    'Image_Effects' : Image_Effects,
                }
                return render(request, template, context)
            else:
                messages.add_message(
                    request, messages.INFO,
                    'Forbidden Page'
                )
                return redirect(reverse('center_listing'))
        else:
            messages.add_message(
                request, messages.ERROR,
                'You need to log in to view this page'
            )
            return redirect(reverse('login'))

@login_required(login_url=LOGIN_URL)
def booking_list_view(request, username):
    merchant_id = request.user.id
    centers = Center.objects.filter(user_id=merchant_id)
    booking_list = list()

    for center in centers:
        bookings = Booking.objects.filter(center_id=center.id)
        for i, booking in enumerate(bookings):
            booking_dict = {
                'booking': booking
            }
            booking_list.append(booking_dict)
    return render(request, "manage_bookings.html", {'booking_list': booking_list})

def booking_action(request, username):
    merchant_id = request.user.id
    centers = Center.objects.filter(user_id=merchant_id)
    booking_list = list()
    ids = list()

    for center in centers:
        bookings = Booking.objects.filter(center_id=center.id)
        for i, booking in enumerate(bookings):
            booking_dict = {
                'booking': booking
            }
            booking_list.append(booking_dict)

    for b_list in booking_list:
        booking_id = b_list.get('booking').id
        ids.append(booking_id)

    for i in ids:
        approve_clicked = request.GET.keys()
        for val in approve_clicked:
            if val == str(i):
                booking = Booking.objects.filter(id=i).get()
                args = dict()
                if booking.is_approved == False:
                    booking.is_approved = True
                    args["email"] = booking.customer_email
                    args["name"] = booking.customer_name
                    booking.save()
                    # send email to customer of approval
                    center = Center.objects.filter(id=booking.center_id).get()

                    booking_approved_email_context = RequestContext(
                        request,
                        {
                            'center_name': center.name,
                            'center_address': center.address,
                            'username': booking.customer_name,
                            'booking': booking.booking_start_date,
                        },
                    )

                    receipient = str(booking.customer_email)

                    subject, from_email, to = 'TheEventDiary: Booking Approved', EMAIL_SENDER, receipient
                    html_content=loader.get_template('booking_approved.html').render(booking_approved_email_context)
                    text_content=loader.get_template('booking_approved.txt').render(booking_approved_email_context)

                    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                    msg.attach_alternative(html_content, "text/html")
                    response = msg.send()

                    if response == 1:
                        messages.add_message(request, messages.INFO, booking.customer_email)

                    return render(request, 'manage_booking_success.html', args)
                else:
                    messages.add_message(
                        request, messages.ERROR,
                        'This request as already being approved by you.'
                    )
                return render(request, "manage_bookings.html", {'booking_list': booking_list})

@login_required(login_url=LOGIN_URL)
def edit_merchant_center(request, username, center_slug=None):
    """Updates information about a center that was created by a merchant.
    """

    center = Center.objects.get(slug=center_slug)
    ImageFormSet = modelformset_factory(CenterPhoto, form=ImageForm)

    if center.user.userprofile.is_merchant != request.user.userprofile.is_merchant:
        messages.add_message(
            request, messages.ERROR,
            'You are not allowed to manage this center'
        )
        return redirect(reverse('center_listing'))

    if request.method == 'POST':
        centerform = CenterForm(request.POST, instance=center)
        formset = ImageFormSet(request.POST, request.FILES, queryset=CenterPhoto.objects.filter(center=center))

        if centerform.is_valid() and formset.is_valid():
            centerform.save(center)
            for form in formset:
                try:
                    image = form.cleaned_data['image']
                    photo = CenterPhoto(center=center, image=image)
                    photo.user_id = request.user.id
                    photo.save()
                except:
                    messages.error(request, 'Technical error')

            messages.add_message(
                request, messages.SUCCESS, 'The Center was updated successfully.'
            )
        else:
            messages.add_message(
                request, messages.ERROR,
                'An error occurred while performing the operation.'
            )
        return redirect(reverse('merchant_manage_centers', kwargs={'username': request.user}))
    else:
        form = CenterForm(instance=center)
        formset = ImageFormSet(queryset=CenterPhoto.objects.filter(center=center))
    return render(request, 'center_edit.html', {'form': form, 'formset': formset})
