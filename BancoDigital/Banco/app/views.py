
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


from django.shortcuts import render, redirect
from .forms import ClienteForm
from django.contrib.auth import login
from django.contrib.auth.hashers import check_password
from .models import Cliente



from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ClienteForm
from django.contrib.auth.hashers import make_password

def registrar(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST, request.FILES)
        if form.is_valid():
            # Criando o cliente, mas sem salvar a senha ainda
            cliente = form.save(commit=False)
            
            # Criptografando a senha antes de salvar
            senha = form.cleaned_data['senha']
            cliente.senha = make_password(senha)
            
            cliente.save()  # Agora salva o cliente com a senha criptografada
            messages.success(request, 'Cliente cadastrado com sucesso!')
            return redirect('success_page')  # Substitua pela URL que deseja redirecionar após o cadastro
        else:
            # Se o formulário não for válido, exibe mensagem de erro
            messages.error(request, 'Erro ao cadastrar cliente. Verifique os campos!')
            return render(request, 'app/registrar.html', {'form': form})
    else:
        form = ClienteForm()  # Se for uma requisição GET, exibe o formulário vazio
    return render(request, 'app/registrar.html', {'form': form})




from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import LoginForm
from .models import Cliente

def logar(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            CPF = form.cleaned_data['CPF']
            senha = form.cleaned_data['senha']
            cliente = Cliente.objects.filter(CPF=CPF).first()
            if cliente and check_password(senha, cliente.senha):
                login(request, cliente)  # Loga o cliente
                return redirect('home')  # Redireciona para a home ou página de sucesso
    else:
        form = LoginForm()
    return render(request, 'app/login.html', {'form': form})


from django.shortcuts import redirect
from django.contrib.auth import logout

def deslogar(request):
    logout(request)  # Realiza o logout do usuário
    return redirect('login') 