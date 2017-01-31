from django import forms
from .models import Merchant

class MerchantForm(forms.ModelForm):

    class Meta:
        model = Merchant
        fields = ['bank_acc_num']

    def save(self, commit=True):

        merchant_user = super(MerchantForm, self).save(commit=False)
        merchant_user.approved = False

        if commit:
            merchant_user.save()
        return merchant_user
