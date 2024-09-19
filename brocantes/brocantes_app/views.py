from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegisterForm, InstituicaoForm, DoadorForm
from .models import User, Cidade, Estado, Instituicao, Doador
from django.http import HttpResponseForbidden, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from brocantes_app.models import Cidade, Estado
from django.core.paginator import Paginator


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

@login_required
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

@login_required
def cadastrar_doador(request):
    estados = Estado.objects.all().order_by('nome')  # Carrega os estados em ordem alfabética
    if request.method == 'POST':
        form = DoadorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Doador gravado com sucesso!')
            #return redirect('lista_doadores')
            return redirect('cadastrar_doador')
    else:
        form = DoadorForm()
    return render(request, 'cadastrar_doador.html', {'form': form, 'estados': estados})

# @login_required
# def listar_doadores(request):
#     doadores = Doador.objects.all()  # Consulta todos os doadores
#     return render(request, 'listar_doadores.html', {'doadores': doadores})


# from django.core.paginator import Paginator
@login_required
def listar_doadores(request):
    doadores_list = Doador.objects.all()
    paginator = Paginator(doadores_list, 10)  # Mostra 10 doadores por página

    page_number = request.GET.get('page')
    doadores = paginator.get_page(page_number)

    return render(request, 'listar_doadores.html', {'doadores': doadores})

@login_required
def excluir_doador(request, doador_id):
    doador = get_object_or_404(Doador, pk=doador_id)

    if request.method == 'POST':
        doador.delete()
        return redirect('listar_doadores')

    return render(request, 'excluir_doador.html', {'doador': doador})

# @login_required
# def editar_doador(request, doador_id):
#     doador = get_object_or_404(Doador, pk=doador_id)

#     if request.method == 'POST':
#         form = DoadorForm(request.POST, instance=doador)
#         if form.is_valid():
#             form.save()
#             return redirect('listar_doadores')  # Redireciona para a lista de doadores após salvar
#     else:
#         form = DoadorForm(instance=doador)

#     return render(request, 'editar_doador.html', {'form': form, 'doador': doador})

@login_required
def editar_doador(request, doador_id):
    doador = get_object_or_404(Doador, pk=doador_id)
    estados = Estado.objects.all()
    cidades = Cidade.objects.filter(estado=doador.estado)

    if request.method == 'POST':
        form = DoadorForm(request.POST, instance=doador)
        if form.is_valid():
            form.save()
            return redirect('listar_doadores')
    else:
        form = DoadorForm(instance=doador)

    return render(request, 'editar_doador.html', {
        'form': form,
        'doador': doador,
        'estados': estados,
        'cidades': cidades
    })
