# from rango.forms import UserForm, UserProfileForm
from .forms import RegistrationForm, LoginForm
from django.shortcuts import render, render_to_response
from django.template import loader, RequestContext

def register(request):
    context = RequestContext(request)
    registered = False

    if request.method == 'POST':
        profile_form = RegistrationForm(data=request.POST)

        if profile_form.is_valid():
            user = profile_form.save()

            user.set_password(user.password)
            user.save()
            return render(request, "initial_done.html")

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        profile_form = RegistrationForm()

    # Render the template depending on the context.
    return render_to_response(
            'user_form.html',
            {'profile_form': profile_form, 'registered': registered},
            context)
