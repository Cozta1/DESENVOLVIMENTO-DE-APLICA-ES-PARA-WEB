from django.views.generic import TemplateView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Conta
from .serializers import ContaSerializer

# Views baseadas em classe para renderizar templates
class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        return context


class TesteView(TemplateView):
    template_name = 'teste.html'

    def get_context_data(self, **kwargs):
        context = super(TesteView, self).get_context_data(**kwargs)
        return context


class SobreView(TemplateView):
    template_name = 'sobre.html'

    def get_context_data(self, **kwargs):
        context = super(SobreView, self).get_context_data(**kwargs)
        return context


class ContatoView(TemplateView):
    template_name = 'contato.html'

    def get_context_data(self, **kwargs):
        context = super(ContatoView, self).get_context_data(**kwargs)
        return context


# API view para listar contas
@api_view(['GET'])
def listar_contas(request):
    contas = Conta.objects.all()
    serializer = ContaSerializer(contas, many=True)
    return Response(serializer.data)