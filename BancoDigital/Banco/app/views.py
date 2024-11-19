
from django.views.generic import TemplateView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Cartao, Conta
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
            return redirect('home')  # Substitua pela URL que deseja redirecionar após o cadastro
        else:
            # Se o formulário não for válido, exibe mensagem de erro
            messages.error(request, 'Erro ao cadastrar cliente. Verifique os campos!')
            return render(request, 'app/registrar.html', {'form': form})
    else:
        form = ClienteForm()  # Se for uma requisição GET, exibe o formulário vazio
    return render(request, 'app/registrar.html', {'form': form})




from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth.models import User


def logar(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cpf = form.cleaned_data['cpf']
            senha = form.cleaned_data['senha']
            
            # Debug: Imprimir os valores para garantir que estão corretos
            print(f"CPF: {cpf}, Senha: {senha}")
            
            # Tente autenticar o usuário com CPF (usuário com 'username' igual ao CPF)
            user = authenticate(request, username=cpf, password=senha)
            
            if user is not None:
                login(request, user)
                return redirect('home')  # Ou qualquer página de redirecionamento após o login
            else:
                form.add_error(None, "CPF ou senha inválidos.")
    else:
        form = LoginForm()

    return render(request, 'app/login.html', {'form': form})






from django.shortcuts import redirect
from django.contrib.auth import logout

def deslogar(request):
    logout(request)  # Realiza o logout do usuário
    return redirect('login') 

################################################################################################

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Conta, Transacao
from django.contrib import messages
from django.http import HttpResponse

@login_required
def gerenciar_conta(request):
    # Recupera a conta do usuário logado
    try:
        conta = Conta.objects.get(cliente=request.user)
    except Conta.DoesNotExist:
        messages.error(request, "Conta não encontrada.")
        # return redirect('home')

    # Recupera as transações da conta do usuário
    transacoes = Transacao.objects.filter(conta=conta).order_by('-data')

    # Verifica se o formulário foi submetido
    if request.method == "POST":
        tipo = request.POST.get('tipo')
        valor = float(request.POST.get('valor', 0))

        if tipo == 'deposito':
            # Realiza o depósito
            conta.saldo += valor
            conta.save()
            # Registra a transação
            transacao = Transacao(conta=conta, tipo='depósito', valor=valor, status='concluído')
            transacao.save()
            messages.success(request, f"Depósito de R$ {valor} realizado com sucesso!")

        elif tipo == 'saque':
            # Realiza o saque, se o saldo for suficiente
            if valor <= conta.saldo:
                conta.saldo -= valor
                conta.save()
                # Registra a transação
                transacao = Transacao(conta=conta, tipo='saque', valor=valor, status='concluído')
                transacao.save()
                messages.success(request, f"Saque de R$ {valor} realizado com sucesso!")
            else:
                messages.error(request, "Saldo insuficiente para o saque.")

        # Após a ação, redireciona para a mesma página para mostrar os resultados
        return redirect('gerenciar_conta')

    # Retorna a página de gerenciamento de conta
    return render(request, 'gerenciar_conta.html', {
        'conta': conta,
        'transacoes': transacoes
    })


#################
from django.shortcuts import render

def home(request):
    print(request.user.is_authenticated)

    if request.user.is_authenticated:
        user = request.user  # Objeto do usuário logado
    else:
        user = None  # Caso não esteja logado, user será None

    return render(request, 'home.html', {'user': user})

#################


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Endereco, Cliente, Agencia, Conta
from .forms import EnderecoForm
from django.contrib import messages

@login_required
def adicionar_endereco(request):
    if request.method == 'POST':
        form = EnderecoForm(request.POST)
        if form.is_valid():
            endereco = form.save(commit=False)
            endereco.cliente = request.user  # Associa o endereço ao cliente logado
            endereco.save()

            # Criar a conta bancária automaticamente para o cliente
            agencia = Agencia.objects.first()  # Você pode personalizar para pegar uma agência aleatória ou específica
            conta = Conta(cliente=request.user, agencia=agencia)
            conta.save()

            # Mensagem de sucesso
            messages.success(request, 'Endereço e conta criados com sucesso!')
            return redirect('home')  # Redireciona para a página principal ou outra página

    else:
        form = EnderecoForm()

    return render(request, 'adicionar_endereco.html', {'form': form})



@login_required
def solicitar_cartao(request):
    conta = Conta.objects.get(cliente=request.user)

    if not hasattr(conta, 'cartao'):  # Verifica se o cliente já possui um cartão
        cartao = Cartao(conta=conta)
        cartao.save()
        messages.success(request, 'Cartão solicitado com sucesso!')
    else:
        messages.error(request, 'Você já possui um cartão vinculado à sua conta.')

    return redirect('gerenciar_conta')  # Redireciona para a página de gerenciamento da conta



