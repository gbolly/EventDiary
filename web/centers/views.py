import cloudinary
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils import timezone
from django.views.generic.base import TemplateView
from django.views.generic import CreateView

from .forms import BookingForm, CenterForm
from .models import Center, Booking


def center_listing(request):
    centers = Center.objects.filter(active=True).order_by('date_last_modified')
    return render(request, 'center_listing.html', {'center': centers})

def center_detail(request, slug):
    center = get_object_or_404(Center, slug=slug)
    return render(request, 'center_detail.html', {
        'center_name': center.name,
        'center_img':center.image,
        'center_description':center.description,
        'center_location':center.state_name,
        'center_price':center.price,
        'center_owner':center.owner,
        'center_capcity':center.capacity,
        'center_address':center.address,
        'center_slug':center.slug,
    })

def booking_view(request, slug, model_class=Center, form_class=BookingForm, template_name='centers/booking_form.html'):
    center = get_object_or_404(model_class, slug=slug)
    args = dict()
    if request.POST:
        form = form_class(request.user, center, request.POST)
        if request.user.is_authenticated():
            if form.is_valid():
                booking = form.save(commit=False)
                booking.center = center
                booking.is_approved = False
                booking.save()
                args["slug"] = slug
                args["center"] = center.name
                return render(request, 'thank_you.html', {"center":center.name})
            else :
                return render(request, template_name, {'form': form})

    else:
        form = form_class(request.user, center)
        return render(request, template_name, {
            'center': center,
            'form': form,
        })

def new_center(request):
    if request.POST:
        form = CenterForm(request.POST)
        if request.user.is_authenticated():
            if form.is_valid():
                center = form.save(commit=False)
                center.owner = request.user
                center.active = True
                center.slug = form.cleaned_data['name'].replace(" ", "")
                center.date_created = timezone.now()
                center.date_last_modified = timezone.now()
                return render(request, 'center_detail.html', {'center': center})
    else:
        form = CenterForm()
        return render(request, 'centers/new_center.html', {'form': form})
