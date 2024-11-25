from django.views.generic import TemplateView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Conta
from .serializers import ContaSerializer


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import ClienteUserCreationForm
from .forms import ClienteLoginForm
from django.contrib.auth import logout

def registro(request):
    if request.method == 'POST':
        form = ClienteUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Loga o usuário após o cadastro
            return redirect('sucesso')  # Redireciona para a página de sucesso
    else:
        form = ClienteUserCreationForm()
    return render(request, 'registro.html', {'form': form})



def sucesso(request):
    return render(request, 'sucesso.html', {'user': request.user})


def login_view(request):
    if request.method == 'POST':
        form = ClienteLoginForm(request.POST)
        if form.is_valid():
            cpf = form.cleaned_data['CPF']
            password = form.cleaned_data['password']
            
            # Tentando autenticar com o CPF e senha
            user = authenticate(request, username=cpf, password=password)
            if user is not None:
                login(request, user)  # Login bem-sucedido
                return redirect('home')  # Redireciona para a página inicial após o login
            else:
                form.add_error(None, 'Credenciais inválidas. Tente novamente.')
    else:
        form = ClienteLoginForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')  # Redireciona para a página inicial após o logout



def home(request):
    return render(request, 'home.html')

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