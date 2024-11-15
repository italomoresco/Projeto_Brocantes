from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegisterForm, InstituicaoForm, DoadorForm, DoacaoForm, DoacaoFilterForm
from .models import User, Cidade, Estado, Instituicao, Doador, Doacao
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
                return redirect('home')  
            else:
                messages.error(request, 'Login ou senha incorretos')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login') 

#@login_required
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
            error_message = "Por favor, selecione o estado e a cidade!"
            return render(request, 'cadastrar_instituicao.html', {'estados': estados, 'error_message': error_message})

        try:
            estado = Estado.objects.get(id=estado_id)
            cidade = Cidade.objects.get(id=cidade_id)

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
def listar_instituicoes(request):
    instituicoes = Instituicao.objects.all()
    return render(request, 'listar_instituicoes.html', {'instituicoes': instituicoes})

@login_required
# def editar_instituicao(request, codigo):
#     instituicao = get_object_or_404(Instituicao, codigo=codigo)
    
#     if request.method == 'POST':
#         form = InstituicaoForm(request.POST, instance=instituicao)
#         if form.is_valid():
#             form.save()
#             return redirect('listar_instituicoes')
#     else:
#         form = InstituicaoForm(instance=instituicao)
    
#     return render(request, 'editar_instituicao.html', {'form': form, 'instituicao': instituicao})

# def editar_instituicao(request, codigo):
#     instituicao = get_object_or_404(Instituicao, codigo=codigo)
#     estados = Estado.objects.all()  # Supondo que você tenha um modelo de estados

#     if request.method == 'POST':
#         instituicao.nome = request.POST.get('nome')
#         instituicao.estado_id = request.POST.get('estado')
#         instituicao.cidade_id = request.POST.get('cidade')
#         instituicao.save()
#         return redirect('listar_instituicoes')

#     return render(request, 'editar_instituicao.html', {'instituicao': instituicao, 'estados': estados})

def editar_instituicao(request, codigo):
    instituicao = get_object_or_404(Instituicao, codigo=codigo)
    estados = Estado.objects.all()
    cidades = Cidade.objects.filter(estado=instituicao.estado)

    if request.method == 'POST':
        instituicao.nome = request.POST.get('nome')
        instituicao.estado_id = request.POST.get('estado')
        instituicao.cidade_id = request.POST.get('cidade')
        instituicao.save()
        return redirect('listar_instituicoes')

    return render(request, 'editar_instituicao.html', {
        'instituicao': instituicao,
        'estados': estados,
        'cidades': cidades  
    })

@login_required
def excluir_instituicao(request, codigo):
    instituicao = get_object_or_404(Instituicao, codigo=codigo)
    
    if request.method == 'POST':
        instituicao.delete()
        return redirect('listar_instituicoes')
    
    return render(request, 'excluir_instituicao.html', {'instituicao': instituicao})


@login_required
def cadastrar_doador(request):
    estados = Estado.objects.all().order_by('nome')  
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

@login_required
def listar_doadores(request):
    doadores_list = Doador.objects.all()
    paginator = Paginator(doadores_list, 10)  

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

@login_required
def cadastrar_doacao(request):
    estados = Estado.objects.all().order_by('nome')
    if request.method == 'POST':
        form = DoacaoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Doação gravada com sucesso!')
            return redirect('listar_doacoes')
    else:
        form = DoacaoForm()

    return render(request, 'cadastrar_doacao.html', {'form': form, 'estados': estados})

@login_required
def listar_doacoes(request):
    doacoes_list = Doacao.objects.all()
    paginator = Paginator(doacoes_list, 10)  

    page_number = request.GET.get('page')
    doacoes = paginator.get_page(page_number)

    return render(request, 'listar_doacoes.html', {'doacoes': doacoes})

@login_required
def excluir_doacao(request, doacao_id):
    doacao = get_object_or_404(Doacao, id=doacao_id)
    
    if request.method == "POST":
        doacao.delete()
        messages.success(request, 'Doação excluída com sucesso!')
        return redirect('listar_doacoes')  
    
    return render(request, 'excluir_doacao.html', {'doacao': doacao})

@login_required
def editar_doacao(request, doacao_id):
    doacao = get_object_or_404(Doacao, id=doacao_id)
    
    if request.method == 'POST':
        form = DoacaoForm(request.POST, instance=doacao)
        if form.is_valid():
            form.save()
            messages.success(request, 'Doação editada com sucesso!')
            return redirect('listar_doacoes')  
    else:
        form = DoacaoForm(instance=doacao)

    return render(request, 'editar_doacao.html', {'form': form, 'doacao': doacao})

def vue_app(request):
    return render(request, 'vue_app.html')  # Certifique-se de que o caminho para o template está correto

def consulta_doacoes(request):
    form = DoacaoFilterForm(request.GET or None)
    doacoes = Doacao.objects.all()

    if form.is_valid():
        if form.cleaned_data['doador']:
            doacoes = doacoes.filter(doador=form.cleaned_data['doador'])
        if form.cleaned_data['numero_controle']:
            doacoes = doacoes.filter(numero_controle__icontains=form.cleaned_data['numero_controle'])
        if form.cleaned_data['ano']:
            doacoes = doacoes.filter(ano=form.cleaned_data['ano'])
        if form.cleaned_data['descricao_arquivo']:
            doacoes = doacoes.filter(descricao_arquivo__icontains=form.cleaned_data['descricao_arquivo'])
        if form.cleaned_data['classificacao']:
            doacoes = doacoes.filter(classificacao__icontains=form.cleaned_data['classificacao'])
        if form.cleaned_data['curso']:
            doacoes = doacoes.filter(curso__icontains=form.cleaned_data['curso'])
        if form.cleaned_data['cidade']:
            doacoes = doacoes.filter(cidade=form.cleaned_data['cidade'])
        if form.cleaned_data['estado']:
            doacoes = doacoes.filter(estado=form.cleaned_data['estado'])

    return render(request, 'consulta_doacoes.html', {'form': form, 'doacoes': doacoes})
