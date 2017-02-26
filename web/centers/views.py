import cloudinary
from cloudinary.forms import cl_init_js_callbacks

from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.core.urlresolvers import reverse
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.template import RequestContext, Engine, loader
from django.utils import timezone
from django.views.generic.list import ListView
from django.forms import modelformset_factory

from .forms import BookingForm, CenterForm, ImageForm
from .models import Center, Booking, State, LocalGovArea, CenterPhoto
from context_processor import Image_Effects


EMAIL_SENDER = 'info@theeventdiary.com'


class CenterListView(ListView):
    model = Center
    template_name = 'center_listing.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(CenterListView, self).get_context_data(**kwargs)
        context['Image_Effects'] = Image_Effects
        return context

    def get_queryset(self):
        center = self.model.objects.all()
        query = self.request.GET.get("q")
        if query:
            center_area = self.model.objects.get_lga_name(query)
            return center.filter(lga=center_area)
        else:
            return center

def center_detail(request, slug):
    center = get_object_or_404(Center, slug=slug)
    photo = CenterPhoto.objects.filter(center_id=center)

    if photo:
        for image in photo:
            image = image.image
    else:
        image = ""

    return render(request, 'center_detail.html', {
        'center_name': center.name,
        'center_description':center.description,
        'center_location':center.state,
        'center_area':center.lga,
        'center_price':center.price,
        'center_owner':center.owner,
        'center_capacity':center.get_facility,
        'center_address':center.address,
        'center_slug':center.slug,
        'Image_Effects':Image_Effects,
        'photo':photo,
        'image':image
    })

def booking_view(request, slug, model_class=Center, form_class=BookingForm, template_name='centers/booking_form.html'):

    cls_default_msgs = {
        'not_signed_in': 'You must be signed in to book this event center',
    }
    center = get_object_or_404(model_class, slug=slug)
    args = dict()

    if request.POST:
        form = form_class(request.user, center, request.POST)
        if request.user.is_authenticated():
            if form.is_valid():
                booking = form.save(commit=False)
                booking.center = center
                booking.user_id = request.user.id
                booking.is_approved = False

                start_date = form.cleaned_data.get("booking_start_date")
                end_date = form.cleaned_data.get("booking_end_date")

                if end_date < start_date:
                    msg = u"The start date cannot be later than the end date. Please input an end date after the selected start date."
                    messages.add_message(request, messages.INFO, msg, form.errors)
                    template = Engine.get_default().get_template(template_name)
                    context = RequestContext(request)
                    return HttpResponse(template.render(context))

                booking.save()
                args["slug"] = slug
                args["center"] = center.name

                # compose the email
                booking_email_context = RequestContext(
                    request,
                    {'username': booking.customer_name,
                     'center': center.name,
                     'booking': booking.booking_start_date,
                    },
                )

                receipient = str(booking.customer_email)

                subject, from_email, to = 'TheEventDiary: Booking Recieved', EMAIL_SENDER, receipient
                html_content=loader.get_template('centers/booking_email.html').render(booking_email_context)
                text_content=loader.get_template('centers/booking_email.txt').render(booking_email_context)

                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                response = msg.send()

                if response == 1:
                    messages.add_message(request, messages.INFO, booking.customer_email)

                return render(request, 'thank_you.html', {"center":center.name})
            else :
                return render(request, template_name, {'form': form})
        else:
            # Set error context
            error_msg = cls_default_msgs['not_signed_in']
            messages.add_message(request, messages.INFO, error_msg, form.errors)
            # Set template
            template = Engine.get_default().get_template('login.html')
            # Set result in RequestContext
            context = RequestContext(request)
            return HttpResponse(template.render(context))

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

    center_form = CenterForm()
    ImageFormSet = modelformset_factory(CenterPhoto, form=ImageForm, extra=3)
    userid = request.user.id
    form = CenterForm(request.POST or None)
    formset = ImageFormSet(request.POST, request.FILES, queryset=CenterPhoto.objects.none())

    if request.POST:
        if request.user.is_authenticated():
            if form.is_valid() and formset.is_valid():
                center = form.save(commit=False)
                center.owner = request.user
                center.user_id = userid
                center.active = True
                center.slug = form.cleaned_data['name'].replace(" ", "")
                center.date_created = timezone.now()
                center.date_last_modified = timezone.now()
                center.save()
                for form in formset.cleaned_data:
                    image = form['image']
                    photo = CenterPhoto(center=center, image=image)
                    photo.user_id = userid
                    photo.save()

                return render(request, "updated_center.html", {"center":center})
        else:
            # Set error context
            error_msg = cls_default_msgs['not_signed_in']
            messages.add_message(request, messages.INFO, error_msg, form.errors)
            # Set template
            template = Engine.get_default().get_template('login.html')
            # Set result in RequestContext
            context = RequestContext(request)
            return HttpResponse(template.render(context))

    return render(request, 'centers/new_center.html', {'form': form, 'formset': ImageFormSet(queryset=CenterPhoto.objects.none())})

@login_required
def edit_center(request, slug=None):
    center = Center.objects.get(slug=slug)
    ImageFormSet = modelformset_factory(CenterPhoto, form=ImageForm)

    if request.user.is_merchant:
        if request.method == 'POST':
            form = CenterForm(request.POST, instance=center)
            formset = ImageFormSet(request.POST, request.FILES, queryset=CenterPhoto.objects.filter(center=center))

            if form.is_valid() and formset.is_valid():
                form.save()
                for form in formset:
                    try:
                        image = form.cleaned_data['image']
                        photo = CenterPhoto(center=center, image=image)
                        photo.user_id = request.user.id
                        photo.save()
                    except:
                        messages.error(request, 'Technical error')
                return render(request, "updated_center.html", locals())
        else:
            form = CenterForm(instance=center)
            formset = ImageFormSet(queryset=CenterPhoto.objects.filter(center=center))
        return render(request, 'center_edit.html', {'form': form, 'formset': formset})
    else:
        messages.add_message(
            request, messages.ERROR,
            'You are not allowed to edit this center. Contact an eventdiary admin'
        )
        return redirect(reverse('center_listing'))
