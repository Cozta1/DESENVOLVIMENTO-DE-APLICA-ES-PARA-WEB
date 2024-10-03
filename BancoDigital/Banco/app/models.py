import uuid
import requests
from django.db.models import Sum


from django.db import models
from stdimage.models import StdImageField
from django.utils.translation import gettext_lazy as _
import random
from datetime import date, timedelta

def get_file_path(_instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return filename

# Create your models here.
from django.db import models


class Endereco(models.Model):
    ESTADO_CHOICES = [
        ('AC', 'AC'),
        ('AL', 'AL'),
        ('AP', 'AP'),
        ('AM', 'AM'),
        ('BA', 'BA'),
        ('CE', 'CE'),
        ('DF', 'DF'),
        ('ES', 'ES'),
        ('GO', 'GO'),
        ('MA', 'MA'),
        ('MT', 'MT'),
        ('MS', 'MS'),
        ('MG', 'MG'),
        ('PA', 'PA'),
        ('PB', 'PB'),
        ('PR', 'PR'),
        ('PE', 'PE'),
        ('PI', 'PI'),
        ('RJ', 'RJ'),
        ('RN', 'RN'),
        ('RS', 'RS'),
        ('RO', 'RO'),
        ('RR', 'RR'),
        ('SC', 'SC'),
        ('SP', 'SP'),
        ('SE', 'SE'),
        ('TO', 'TO'),
    ]
    
    cep = models.CharField(_('CEP'), max_length=8)
    rua = models.CharField(_('Rua'), max_length=100)
    bairro = models.CharField(_('Bairro'), max_length=50)
    cidade = models.CharField(_('Cidade'), max_length=50)
    estado = models.CharField(_('Estado'), max_length=2, choices=ESTADO_CHOICES)
    numero = models.CharField(_('Número'), max_length=10)
    complemento = models.CharField(_('Complemento'), max_length=50)
    
    def preencher_endereco_por_cep(self):
        if self.cep:
            url = f"https://viacep.com.br/ws/{self.cep}/json/"
            response = requests.get(url)
            if response.status_code == 200:
                dados = response.json()
                self.rua = dados.get('logradouro', '')
                self.bairro = dados.get('bairro', '')
                self.cidade = dados.get('localidade', '')
                self.estado = dados.get('uf', '')
    
    # seria legal fazer o cep ja adicionar os outros campos, mas n sei o quao comlicado é 
    
    class Meta:
        verbose_name = _('Endereço')
        verbose_name_plural = _('Endereços')

    def __str__(self):
        return f'{self.bairro} - {self.rua} - {self.numero}'

##########################################################################################

class Cliente(models.Model):
    CPF = models.CharField(_('CPF'), max_length=11, unique=True, primary_key=True)
    nome = models.CharField(_('Nome'), max_length=100)
    email = models.EmailField(_('E-Mail'), blank=True, null=True)
    telefone = models.CharField(_('Telefone'), max_length=15, blank=True, null=True)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)
    senha = models.CharField(_('Senha'), max_length=255)
    dataCadastro = models.DateTimeField( auto_now_add=True)
    foto = StdImageField(_('Foto'), null=True, blank=True, upload_to=get_file_path, variations={'thumb': {'width': 480, 'height': 480, 'crop': True}})
    
    class Meta:
        verbose_name = _('Cliente')
        verbose_name_plural = _('Clientes')

    def __str__(self):
        return self.nome

##########################################################################################

class Agencia(models.Model):
    nomeagencia = models.CharField(_('Nome da Agência'), max_length=100, null=False)
    numeroagencia = models.AutoField(primary_key=True, unique=True, editable=False, null=False)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)

# gerar numero da agencia comecando no 1 e adicionando 1

    class Meta:
        verbose_name = _('Agencia')
        verbose_name_plural = _('Agencias')
        
    def __str__(self):
        return self.nomeagencia
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

##########################################################################################

class Conta(models.Model):
    numeroConta = models.AutoField(_('Número da Conta'), primary_key=True, unique=True, editable=False, null=False)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    agencia = models.ForeignKey(Agencia, on_delete=models.CASCADE)
    dataAbertura = models.DateField(_('Data de Abertura'), auto_now_add=True)

    @property
    def saldo(self):
        # Somar os depósitos e transferências recebidas
        total_creditos = self.transacoes.filter(
            tipoTransacao__in=['deposito', 'transferencia'],
            status='concluida',
            contaDestino=self
        ).aggregate(Sum('valor'))['valor__sum'] or 0

        # Subtrair os saques e transferências enviadas
        total_debitos = self.transacoes.filter(
            tipoTransacao__in=['saque', 'transferencia'],
            status='concluida',
            conta=self
        ).aggregate(Sum('valor'))['valor__sum'] or 0

        # O saldo final é a diferença entre os créditos e débitos
        saldo_atual = total_creditos - total_debitos
        return saldo_atual

    def depositar(self, valor):
        if valor <= 0:
            raise ValueError("O valor do depósito deve ser positivo.")
        # Aqui você pode criar uma transação de depósito, se necessário.
        Notificacao.objects.create(
            conta=self,
            mensagem=f"Depósito de {valor} realizado com sucesso."
        )

    def sacar(self, valor):
        if valor <= 0:
            raise ValueError("O valor do saque deve ser positivo.")
        if self.saldo < valor:
            raise ValueError("Saldo insuficiente para realizar o saque.")
        # Aqui você pode criar uma transação de saque, se necessário.
        Notificacao.objects.create(
            conta=self,
            mensagem=f"Saque de {valor} realizado com sucesso."
        )

    def transferir(self, contaDestino, valor):
        if valor <= 0:
            raise ValueError("O valor da transferência deve ser positivo.")
        if self.saldo < valor:
            raise ValueError("Saldo insuficiente para realizar a transferência.")
        # Realizar a transferência
        contaDestino.depositar(valor)
        self.sacar(valor)
        # Gerar notificação de transferência
        Notificacao.objects.create(
            conta=self,
            mensagem=f"Transferência de {valor} para a conta {contaDestino.numeroConta} realizada com sucesso."
        )

    class Meta:
        verbose_name = _('Conta')
        verbose_name_plural = _('Contas')

    def __str__(self):
        return f'{self.cliente.nome} - {self.saldo}'

##########################################################################################

class Transacao(models.Model):
    numeroTransacao = models.AutoField(_('Número da Transação'), primary_key=True)  # Novo campo
    # cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)  # Removido conforme solicitado
    conta = models.ForeignKey(Conta, on_delete=models.CASCADE, related_name='transacoes')
    contaDestino = models.ForeignKey(Conta, on_delete=models.CASCADE, related_name='transacoes_destino', null=True, blank=True)
    valor = models.DecimalField(_('Valor'), max_digits=10, decimal_places=2)
    tipoTransacao = models.CharField(_('Tipo de Transação'), max_length=50, choices=[
        ('deposito', 'Depósito'),
        ('saque', 'Saque'),
        ('transferencia', 'Transferência')
    ])
    status = models.CharField(_('Status'), max_length=20, default='pendente')
    dataHora = models.DateTimeField(_('Data e Hora da Transação'), auto_now_add=True, null=True)  # Campo existente

    def save(self, *args, **kwargs):
    # Verificar se o saldo é suficiente para saque ou transferência
        if self.tipoTransacao in ['saque', 'transferencia']:
            if self.conta.saldo < self.valor:
                self.status = 'cancelada'
                # Gerar notificação de saldo insuficiente
                Notificacao.objects.create(
                    cliente=self.conta.cliente,  # Associar o cliente corretamente
                    mensagem="Transação cancelada: Saldo insuficiente."
                )
                super().save(*args, **kwargs)  # Salvar a transação com status cancelado
                return  # Saia da função se o saldo for insuficiente

        # Se o saldo for suficiente ou se for um depósito, proceda
        if self.tipoTransacao == 'saque':
            self.conta.sacar(self.valor)  # Chame o método de saque
        elif self.tipoTransacao == 'deposito':
            self.conta.depositar(self.valor)  # Chame o método de depósito
        elif self.tipoTransacao == 'transferencia':
            if self.contaDestino:
                self.conta.transferir(self.contaDestino, self.valor)  # Chame o método de transferência

        # Salvar a transação com status concluído
        self.status = 'concluida'  # Define o status como concluído
        super().save(*args, **kwargs)  # Salvar a transação

        # Gerar notificação de sucesso
        Notificacao.objects.create(
            cliente=self.conta.cliente,  # Associar o cliente corretamente
            mensagem=f"Transação {self.tipoTransacao} concluída com sucesso."
        )

    class Meta:
        verbose_name = _('Transação')
        verbose_name_plural = _('Transações')

    def __str__(self):
        return f'Transação {self.numeroTransacao}: {self.tipoTransacao} de {self.valor} em {self.dataHoraTransacao}'
##########################################################################################

# a geração aleatoria do cartao foi feita com ajuda de IA (pra deixar claro)
class Cartao(models.Model):
    BANDEIRAS = [
        ('visa', 'Visa'),
        ('elo', 'Elo'),
        ('mastercard', 'MasterCard'),
    ]

    numeroCartao = models.BigIntegerField(_('Numero do Cartão'), unique=True, blank=True, editable=False)  # Defina como blank=True para que possa ser gerado
    conta = models.ForeignKey(Conta, on_delete=models.CASCADE)
    bandeira = models.CharField(_('Bandeira'), max_length=20, choices=BANDEIRAS, default='visa')
    dataExpiracao = models.DateField(_('Data de Expiração'), blank=True, editable=False)  # Permita que seja gerada
    cvv = models.IntegerField(_('CVV'), blank=True, editable=False)  # Permita que seja gerado


    class Meta:
        verbose_name = _('Cartão')
        verbose_name_plural = _('Cartões')

    def save(self, *args, **kwargs):
        if not self.numeroCartao:
            self.numeroCartao = self.gerar_numero_cartao()
        if not self.cvv:
            self.cvv = random.randint(100, 999)
        if not self.dataExpiracao:
            self.dataExpiracao = date.today() + timedelta(days=365*4)

        super().save(*args, **kwargs)

    def gerar_numero_cartao(self):
        if self.bandeira == 'visa':
            prefix = '4'
        elif self.bandeira == 'mastercard':
            prefix = '5'
        elif self.bandeira == 'elo':
            prefix = '6'
        else:
            raise ValueError("Bandeira inválida")

        numero_aleatorio = ''.join([str(random.randint(0, 9)) for _ in range(15)])
        return int(prefix + numero_aleatorio)

    def __str__(self):
        return f"{self.bandeira.upper()} - {str(self.numeroCartao)}"


##########################################################################################

class Notificacao(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)  # Campo cliente
    dataHora = models.DateTimeField(auto_now_add=True)
    mensagem = models.TextField()
    status = models.CharField(max_length=20, default='pendente')

    class Meta:
        verbose_name = _('Notificação')
        verbose_name_plural = _('Notificações')
    
    def __str__(self):
        return f'Notificação para {self.cliente}: {self.mensagem}'