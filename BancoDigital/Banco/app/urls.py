from django import views
from django.urls import path
from .views import IndexView, TesteView, ContatoView, SobreView, listar_contas  # Importe listar_contas aqui
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('teste/', TesteView.as_view(), name='teste'),  # Adicione barra '/' ao final dos paths para manter o padrão
    path('sobre/', SobreView.as_view(), name='sobre'),
    path('contato/', ContatoView.as_view(), name='contato'),
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('sucesso/', views.sucesso, name='sucesso'),
    path('logout/', views.logout_view, name='logout'),
]