import cloudinary
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, render_to_response
from django.template import RequestContext, Engine
from django.utils import timezone
from django.contrib import messages
from django.views.generic.list import ListView

from .forms import BookingForm, CenterForm
from .models import Center, Booking

class CenterListView(ListView):
    model = Center
    template_name = 'center_listing.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(CenterListView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        center = self.model.objects.all()
        query = self.request.GET.get("q")
        center_area = self.model.objects.get_area_name(query)
        if query:
            return center_area
        else:
            return center

def center_detail(request, slug):
    center = get_object_or_404(Center, slug=slug)
    return render(request, 'center_detail.html', {
        'center_name': center.name,
        'center_img':center.image,
        'center_description':center.description,
        'center_location':center.state_name,
        'center_area':center.area_name,
        'center_price':center.price,
        'center_owner':center.owner,
        'center_capacity':center.capacity,
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
    cls_default_msgs = {
        'not_signed_in': 'You must be signed in to list your event center',
        'invalid_param': 'Invalid parameters. \
                        Please make sure you fill in all fields',
    }

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
                center.save()
                return render(request, 'center_detail.html', {
                    'center_name': center.name,
                    'center_img':center.image,
                    'center_description':center.description,
                    'center_location':center.state_name,
                    'center_area':center.area_name,
                    'center_price':center.price,
                    'center_owner':center.owner,
                    'center_capacity':center.capacity,
                    'center_address':center.address,
                    'center_slug':center.slug,
                })
        else:
            # Set error context
            error_msg = cls_default_msgs['not_signed_in']
            messages.add_message(request, messages.INFO, error_msg)

            # Set template
            template = Engine.get_default().get_template(
                'login.html')

            # Set result in RequestContext
            context = RequestContext(request)
            return HttpResponse(template.render(context))
    else:
        form = CenterForm()
        return render(request, 'centers/new_center.html', {'form': form})
