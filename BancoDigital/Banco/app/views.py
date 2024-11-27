from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import ClienteUserCreationForm
from .forms import ClienteLoginForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import EnderecoForm
from .models import Agencia, Cartao, Conta, Endereco, Transacao


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
    # Buscar os cartões associados ao cliente logado
    cartoes = Cartao.objects.filter(cliente=request.user)

    return render(request, 'conta.html', {'cartoes': cartoes}) 



@login_required
def cadastrar_endereco(request):
    if request.method == 'POST':
        form = EnderecoForm(request.POST)
        if form.is_valid():
            endereco = form.save(commit=False)
            endereco.cliente = request.user  # Relaciona o endereço ao usuário logado
            endereco.save()
            return redirect('perfil')  # Redireciona para a página de seleção de agência
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


def excluir_endereco(request, endereco_id):
    endereco = get_object_or_404(Endereco, id=endereco_id, cliente=request.user)
    endereco.delete()
    return redirect('perfil')  # Redireciona para o perfil do usuário


@login_required
def solicitar_cartao(request):
    if request.method == 'POST':
        # Obtém os dados do formulário
        conta_id = request.POST.get('conta')
        bandeira = request.POST.get('bandeira')

        # Verifica se a conta existe
        try:
            conta = Conta.objects.get(numeroConta=conta_id, cliente=request.user)
        except Conta.DoesNotExist:
            # Caso não exista, você pode redirecionar ou mostrar uma mensagem de erro
            return render(request, 'solicitar_cartao.html', {'error': 'Conta não encontrada.'})

        # Cria um novo cartão
        cartao = Cartao(conta=conta, bandeira=bandeira)
        cartao.save()  # O cliente será atribuído automaticamente aqui

        # Passa o cartão solicitado para o template para exibição
        return render(request, 'solicitar_cartao.html', {
            'cartao_solicitado': cartao,
            'contas': Conta.objects.filter(cliente=request.user)  # Apenas contas do cliente logado
        })

    # Exibe o formulário de solicitação de cartão
    contas = Conta.objects.filter(cliente=request.user)
    return render(request, 'solicitar_cartao.html', {'contas': contas})


@login_required
def transacao_view(request):
    if request.method == 'POST':
        tipo_transacao = request.POST.get('tipo_transacao')
        valor = request.POST.get('valor')
        conta_destino_id = request.POST.get('conta_destino') if tipo_transacao == 'transferencia' else None
        
        # Recuperar a conta do cliente logado
        conta = Conta.objects.get(cliente=request.user)
        
        if tipo_transacao == 'saque':
            # Criar uma transação de saque
            transacao = Transacao(conta=conta, tipoTransacao='saque', valor=valor)
            transacao.save()
        elif tipo_transacao == 'deposito':
            # Criar uma transação de depósito
            transacao = Transacao(conta=conta, tipoTransacao='deposito', valor=valor)
            transacao.save()
        elif tipo_transacao == 'transferencia':
            # Criar uma transação de transferência
            conta_destino = Conta.objects.get(id=conta_destino_id)
            transacao = Transacao(conta=conta, contaDestino=conta_destino, tipoTransacao='transferencia', valor=valor)
            transacao.save()

        # Redirecionar para a página de conta após a transação
        return redirect('conta')

    return render(request, 'transacao.html')
