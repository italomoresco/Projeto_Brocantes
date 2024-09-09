from django import forms
from .models import User, Instituicao, Estado, Cidade

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

class InstituicaoForm(forms.ModelForm):
    estado = forms.ModelChoiceField(queryset=Estado.objects.all(), label="Estado")
    cidade = forms.ModelChoiceField(queryset=Cidade.objects.none(), label="Cidade")

    class Meta:
        model = Instituicao
        fields = ['nome', 'estado', 'cidade']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'estado' in self.data:
            try:
                estado_id = int(self.data.get('estado'))
                self.fields['cidade'].queryset = Cidade.objects.filter(estado_id=estado_id).order_by('nome')
            except (ValueError, TypeError):
                pass  # Se o estado for inválido, retorna um queryset vazio.
        elif self.instance.pk:
            self.fields['cidade'].queryset = self.instance.estado.cidades.order_by('nome')

