from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View

from django.shortcuts import render
from web.centers.models import Center

class ManageCenterView(View):
    """Manage a single center"""

    def get(self, request, center_slug):
        """Renders a page showing a center that was created by a merchant
        """
        center = get_object_or_404(Center, slug=center_slug)
        if Center.user != request.user.is_merchant:
            messages.add_message(
                request, messages.ERROR,
                'You are not allowed to manage this center'
            )
            return redirect(reverse('merchant_manage_centers'))
        context_data = {
            'center': center,
            'breadcrumbs': [
                {'name': 'Merchant', 'url': reverse('merchant_manage_centers')},
                {'name': 'Centers', }
            ]
        }
        return render(request, 'center.html', context_data)

    # def post(self, request, deal_slug):
    #     """Updates information about a deal that was created by a merchant.
    #     """
    #     dealform = DealForm(request.POST, request.FILES)
    #     deal = get_object_or_404(Deal, slug=deal_slug)
    #     if deal.advertiser != request.user.profile.merchant.advertiser_ptr:
    #         messages.add_message(
    #             request, messages.ERROR,
    #             'You are not allowed to manage this deal'
    #         )
    #         return redirect(reverse('merchant_manage_deals'))

    #     if dealform.is_valid():
    #         dealform.save(deal)
    #         messages.add_message(
    #             request, messages.SUCCESS, 'The deal was updated successfully.'
    #         )
    #     else:
    #         messages.add_message(
    #             request, messages.ERROR,
    #             'An error occurred while performing the operation.'
    #         )
    #     return redirect(
    #         reverse('merchant_manage_deal', kwargs={'deal_slug': deal.slug})
    #     )
