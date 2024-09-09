from django import forms
from .models import User

class LoginForm(forms.Form):
    username = forms.CharField(label='Login', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    remember_me = forms.BooleanField(label='Lembre-me', required=False)

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ['name', 'login', 'password']

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=True)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user