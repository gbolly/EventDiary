from django import forms
from .models import User

class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(widget = forms.TextInput, label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    # password2 = forms.CharField(widget=forms.PasswordInput, label="Password (again)")
    class Meta:
        model = User
        fields = ['email', 'password']

    def clean(self):
            """
            Verifies that the values entered into the password fields match

            NOTE: Errors here will appear in ``non_field_errors()`` because it applies to more than one field.
            """
            # cleaned_data = super(RegistrationForm, self).clean()
            # if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            #     if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            #         raise forms.ValidationError("Passwords don't match. Please enter both fields again.")
            # return self.cleaned_data

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    """docstring for Login"""
    email = forms.EmailField(widget=forms.widgets.TextInput)
    password = forms.CharField(widget=forms.widgets.PasswordInput)

    class Meta:
        fields = ['email', 'password']
        
