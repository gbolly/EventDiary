from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View

from django.shortcuts import render
from django.contrib.auth.models import User
from django.forms import modelformset_factory

from web.centers.baseviews import CenterListBaseView
from web.centers.forms import CenterForm, ImageForm
from web.centers.models import Center, CenterPhoto
from web.centers.context_processor import Image_Effects

class ManageCenterView(CenterListBaseView):
    """Manage a single center"""

    def get(self, request, username):
        """Renders a page showing a center that was created by a merchant
        """

        list_title = "My Centers"
        list_description = "All centers posted by you"
        merchant_user = request.user.userprofile.is_merchant
        template = "center.html"

        if merchant_user:
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
                request, messages.ERROR,
                'Forbidden Page'
            )
            return redirect(reverse('center_listing'))

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
