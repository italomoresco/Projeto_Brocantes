from django.urls import path
from . import views
from .views import cidades_por_estado, cadastrar_doador, editar_doador, excluir_doador, cadastrar_doacao

urlpatterns = [
    path('', views.home, name='home'),
    # path('', views.consulta_doacoes, name='consulta_doacoes'),  
    path('app/', views.vue_app, name='vue_app'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('cadastrar_instituicao/', views.cadastrar_instituicao, name='cadastrar_instituicao'),    
    path('ajax/carrega_cidades/', views.ajax_carrega_cidades, name='ajax_carrega_cidades'),
    path('cidades_por_estado/<int:estado_id>/', cidades_por_estado, name='cidades_por_estado'),
    path('cadastrar_doador/', cadastrar_doador, name='cadastrar_doador'),
    path('doadores/', views.listar_doadores, name='listar_doadores'),
    path('editar_doador/<int:doador_id>/', editar_doador, name='editar_doador'),
    path('excluir_doador/<int:doador_id>/', excluir_doador, name='excluir_doador'),
    path('cadastrar_doacao/', cadastrar_doacao, name='cadastrar_doacao'),
    path('doacoes/',views.listar_doacoes, name='listar_doacoes'),
    path('excluir_doacao/<int:doacao_id>/', views.excluir_doacao, name='excluir_doacao'),
    path('editar_doacao/<int:doacao_id>/', views.editar_doacao, name='editar_doacao'),
    path('instituicoes/', views.listar_instituicoes, name='listar_instituicoes'),
    path('instituicoes/editar/<int:codigo>/', views.editar_instituicao, name='editar_instituicao'),
    path('instituicoes/excluir/<int:codigo>/', views.excluir_instituicao, name='excluir_instituicao'),
    path('consulta_doacoes/', views.consulta_doacoes, name='consulta_doacoes'),
]


