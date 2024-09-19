from django.urls import path
from . import views
from .views import cidades_por_estado, cadastrar_doador

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('cadastrar_instituicao/', views.cadastrar_instituicao, name='cadastrar_instituicao'),    
    path('ajax/carrega_cidades/', views.ajax_carrega_cidades, name='ajax_carrega_cidades'),
    path('cidades_por_estado/<int:estado_id>/', cidades_por_estado, name='cidades_por_estado'),
    path('cadastrar_doador/', cadastrar_doador, name='cadastrar_doador'),
]
