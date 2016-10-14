# import pyotp
# from nexmo.libpynexmo.nexmomessage import NexmoMessage
import StringIO
import time

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import redirect, get_object_or_404, render
from django.template import RequestContext
from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView
from django.utils.text import slugify

from web.accounts.forms import UserProfileForm
from web.accounts.models import UserProfile
from web.authentication.views import LoginRequiredMixin

from web.centers.models import ALL_LOCATIONS, NIGERIAN_LOCATIONS


class UserProfileView(LoginRequiredMixin, TemplateView):
    """
    Handles display of the account profile form view
    """
    form_class = UserProfileForm
    template_name = "account/profile.html"

    def get_context_data(self, **kwargs):
        context_var = super(UserProfileView, self).get_context_data(**kwargs)
        context_var.update({
            'profile': self.request.user.profile,
            'locations': {
                'choices': NIGERIAN_LOCATIONS, 'default': 25
            },
            'breadcrumbs': [
                {'name': 'My Account', 'url': reverse('account')},
                {'name': 'Profile', },
            ]
        })
        return context_var

    def post(self, request, **kwargs):

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        profile = UserProfile.objects.get(id=request.user.profile.id)
        form_dict = profile.check_diff(request.POST)

        form = self.form_class(
            form_dict, instance=request.user.profile)

        if form.errors:
            context_var = {}
            empty = "Form should not be submitted empty"
            messages.add_message(request, messages.INFO, empty)
            return TemplateResponse(
                request, 'account/profile.html', context_var
            )

        if form.is_valid():
            form.save()

            user = User.objects.get(id=request.user.id)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            messages.add_message(
                request, messages.SUCCESS, 'Profile Updated!')
            return redirect(
                reverse('account_profile'),
                context_instance=RequestContext(request)
            )
