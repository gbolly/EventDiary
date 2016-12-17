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
    return render(request, 'center_detail.html', {'center': center})

def booking_view(request, slug, model_class=Center, form_class=BookingForm, template_name='centers/booking_form.html'):
    center = get_object_or_404(model_class, slug=slug)

    if request.POST:
        form = form_class(request.user, center, request.POST)
        
        if form.is_valid():
            booking = form.save()
            # change the redirect page to a thank you page
            return HttpResponseRedirect(reverse('center_detail', kwargs={'slug': slug}))
        else :
            return render(request, 'centers/booking_form.html', {'form': form})

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
                print center.slug
                center.date_created = timezone.now()
                center.date_last_modified = timezone.now()
                center.save()
                print "saved=============="
                return render(request, 'center_detail.html', {'center': center})
    else:
        form = CenterForm()
        return render(request, 'centers/new_center.html', {'form': form})
        

    # ------ MIXINS ------ #

# class BookingViewMixin(object):
#     model = Booking
#     form_class = BookingForm

# ------ MODEL VIEWS ------ #

# class BookingCreateView(BookingViewMixin, CreateView):
#     """View to create a new ``Booking`` instance."""
#     def get_success_url(self):
#         return reverse('booking_create', kwargs={'pk': self.object.pk})

#     def get_form_kwargs(self, *args, **kwargs):
#         kwargs = super(BookingCreateView, self).get_form_kwargs(
#             *args, **kwargs)
#         if self.request.user.is_authenticated():
#             kwargs.update({'user': self.request.user})
#         else:
#             # If the user is not authenticated, get the current session
#             if not self.request.session.exists(
#                     self.request.session.session_key):
#                 self.request.session.create()
#             kwargs.update({'session': Session.objects.get(
#                 session_key=self.request.session.session_key)})
#             print kwargs
#         return kwargs
