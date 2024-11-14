from django import forms
from .models import User, Instituicao, Estado, Cidade, Doador, Doacao

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

class DoadorForm(forms.ModelForm):
    class Meta:
        model = Doador
        fields = ['nome', 'email', 'telefone', 'documento_id', 'cidade', 'estado']

class DoacaoForm(forms.ModelForm):
    class Meta:
        model = Doacao
        fields = [
            'doador', 'numero_controle', 'link_documento_original', 
            'link_documento_tajado', 'descricao_arquivo', 'ano', 
            'paginas', 'largura', 'comprimento', 'classificacao', 
            'nivel', 'curso', 'instituicao', 'cidade', 'estado', 
            'observacao', 'digitalizado', 'devolucao', 'recebido', 'publicado'
        ]        

class DoacaoFilterForm(forms.Form):
    doador = forms.ModelChoiceField(queryset=Doador.objects.all(), required=False, label="Doador")
    numero_controle = forms.CharField(max_length=30, required=False, label="Número de Controle")
    ano = forms.IntegerField(required=False, label="Ano")
    descricao_arquivo = forms.CharField(max_length=200, required=False, label="Descrição do Arquivo")
    classificacao = forms.CharField(max_length=50, required=False, label="Classificação")
    curso = forms.CharField(max_length=50, required=False, label="Curso")
    cidade = forms.ModelChoiceField(queryset=Cidade.objects.all(), required=False, label="Cidade")
    estado = forms.ModelChoiceField(queryset=Estado.objects.all(), required=False, label="Estado")
