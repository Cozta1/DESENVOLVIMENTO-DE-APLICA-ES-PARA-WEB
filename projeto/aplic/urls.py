from django.urls import path

from .views import IndexView, TesteView, ContatoView, SobreView
from rest_framework.routers import SimpleRouter


router = SimpleRouter()

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('teste', TesteView.as_view(), name='teste'),
    path('sobre', SobreView .as_view(), name='sobre'),
    path('contato', ContatoView.as_view(), name='contato'),
]