import datetime

from django.views.generic import View
from django.template import RequestContext, loader
from django.template.response import TemplateResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

from models import Center


class CenterListBaseView(View):
    """
    Base class for other Center listing views.
    It implements a default 'get' method allowing
    subclassing views to render fully functional
    Center listings by simply overriding the default
    class level options.
    Subclassing views can still override and implement
    their own get or post methods. However these methods
    can call the base 'render_center_list' method which
    returns the rendered Center list as a string.
    """

    # default Center list options as class level vars:
    queryset = Center.objects.all()  # can be any queryset of Center instances *
    title = "Centers"
    description = ""
    username = ""
    zero_items_message = "Sorry, no centers found!"
    num_page_items = 15
    min_orphan_items = 2
    show_page_num = 1
    pagination_base_url = ""

    def render_center_list(self, request, **kwargs):
        """ Takes a queryset of center
        """

        # update the default options with any specified as kwargs:
        for arg_name in kwargs:
            try:
                setattr(self, arg_name, kwargs.get(arg_name))
            except:
                pass

        # set the context and render the template to a string:
        centers_list_context = RequestContext(request, {'listing': self.get_queryset(),})
        return centers_list_context

    def get_queryset(self):
        """ returns the default centers queryset.
            override this method to return custom querysets.
        """
        return self.queryset

    def get(self, request, *args, **kwargs):
        """ returns a full featured centers-listing page showing
            the centers set in 'centers' class variable.
        """
        context = {
            'rendered_center_list': self.render_center_list(request),
        }
        return TemplateResponse(request, 'center.html', context)
