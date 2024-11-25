from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import ClienteUserCreationForm
from .forms import ClienteLoginForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import EnderecoForm
from .models import Agencia, Conta, Endereco


def registro(request):
    if request.method == 'POST':
        form = ClienteUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Loga o usuário após o cadastro
            return redirect('cadastrar_endereco')  # Redireciona para a página de cadastro de endereço
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



@login_required
def conta_view(request):
    if request.method == 'POST':
        saque = request.POST.get('saque')
        deposito = request.POST.get('deposito')
        conta_destino = request.POST.get('conta_destino')
        valor_transferencia = request.POST.get('valor_transferencia')

        # Lógica para realizar transações (só exemplo)
        if saque:
            # Processar o saque (reduzir saldo, etc.)
            pass
        if deposito:
            # Processar o depósito (adicionar saldo, etc.)
            pass
        if conta_destino and valor_transferencia:
            # Processar a transferência
            pass

        return redirect('conta')  # Redireciona de volta à página da conta

    return render(request, 'conta.html')  # Exibe a página da conta



@login_required
def cadastrar_endereco(request):
    if request.method == 'POST':
        form = EnderecoForm(request.POST)
        if form.is_valid():
            endereco = form.save(commit=False)
            endereco.cliente = request.user  # Relaciona o endereço ao usuário logado
            endereco.save()
            return redirect('selecionar_agencia')  # Redireciona para a página de seleção de agência
    else:
        form = EnderecoForm()

    return render(request, 'cadastrar_endereco.html', {'form': form})



@login_required
def selecionar_agencia(request):
    if request.method == 'POST':
        agencia_id = request.POST.get('agencia')
        
        # A consulta agora usa o campo numeroagencia
        agencia = Agencia.objects.get(numeroagencia=agencia_id)
        
        # Cria uma conta associada ao cliente e à agência selecionada
        cliente = request.user
        Conta.objects.create(cliente=cliente, agencia=agencia)
        
        return redirect('perfil')  # Redireciona para a página de perfil após a criação da conta
    
    agencias = Agencia.objects.all()  # Pega todas as agências
    return render(request, 'selecionar_agencia.html', {'agencias': agencias})



@login_required
def perfil(request):
    cliente = request.user
    contas = Conta.objects.filter(cliente=cliente)  # Obtém todas as contas do cliente
    agencias = Agencia.objects.all()  # Obtém todas as agências para a criação de novas contas
    
    if request.method == 'POST':
        # Lógica para criar nova conta
        agencia_id = request.POST.get('agencia')
        agencia = Agencia.objects.get(id=agencia_id)  # Seleciona a agência pela ID # Função para gerar número de conta, pode ser qualquer lógica
        Conta.objects.create(cliente=cliente, agencia=agencia)
        return redirect('perfil')  # Redireciona para o perfil após criar a conta
    
    return render(request, 'perfil.html', {
        'cliente': cliente,
        'enderecos': Endereco,
        'contas': contas,
        'agencias': agencias
    })
