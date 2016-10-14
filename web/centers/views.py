from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic.base import TemplateView
from .models import Center

# Create your views here.
def center_listing(request):
    centers = Center.objects.filter(date_last_modified__lte=timezone.now()).order_by('location')
    return render(request, 'center_listing.html', {'center': centers})

def center_detail(request, name):
    center = get_object_or_404(Center, name=name)
    return render(request, 'center_detail.html', {'center': center})
