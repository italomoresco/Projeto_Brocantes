from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegisterForm, InstituicaoForm
from .models import User, Cidade, Estado, Instituicao
from django.http import HttpResponseForbidden, JsonResponse
from brocantes_app.models import Cidade, Estado

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirecionar para a página inicial após o login bem-sucedido
            else:
                messages.error(request, 'Login ou senha incorretos')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirecionar para a página de login após o logout

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def register_view(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Você não tem permissão para acessar esta página.")

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

# @login_required
# def cadastrar_instituicao(request):
#     if request.method == 'POST':
#         form = InstituicaoForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = InstituicaoForm()

#     estados = Estado.objects.all().order_by('nome')

#     return render(request, 'cadastrar_instituicao.html', {'form': form, 'estados': estados})

def cadastrar_instituicao(request):
    estados = Estado.objects.all().order_by('nome')
    
    if request.method == 'POST':
        estado_id = request.POST.get('estado')
        cidade_id = request.POST.get('cidade')
        nome_instituicao = request.POST.get('nome')

        if not estado_id or not cidade_id:
            # Verifica se o estado ou a cidade não foram selecionados
            error_message = "Por favor, selecione o estado e a cidade!"
            return render(request, 'cadastrar_instituicao.html', {'estados': estados, 'error_message': error_message})

        try:
            estado = Estado.objects.get(id=estado_id)
            cidade = Cidade.objects.get(id=cidade_id)

            # Cria a instituição apenas se ambos estiverem válidos
            Instituicao.objects.create(nome=nome_instituicao, estado=estado, cidade=cidade)
            #return redirect('instituicoes_list')
            return redirect('home')

        except (Estado.DoesNotExist, Cidade.DoesNotExist):
            error_message = "Estado ou Cidade inválidos."
            return render(request, 'cadastrar_instituicao.html', {'estados': estados, 'error_message': error_message})

    return render(request, 'cadastrar_instituicao.html', {'estados': estados})


def ajax_carrega_cidades(request):
    estado_id = request.GET.get('estado_id')
    cidades = Cidade.objects.filter(estado_id=estado_id).order_by('nome')
    return render(request, 'cidades_dropdown_list_options.html', {'cidades': cidades})

def cidades_por_estado(request, estado_id):
    cidades = Cidade.objects.filter(estado_id=estado_id).values('id', 'nome')
    return JsonResponse({'cidades': list(cidades)})    

