import uuid

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
    
    # seria legal fazer o cep ja adicionar os outros campos, mas n sei o quao comlicado é 
    
    class Meta:
        verbose_name = _('Endereço')
        verbose_name_plural = _('Endereços')

    def __str__(self):
        return f'{self.bairro} - {self.rua} - {self.numero}'

##########################################################################################

class Cliente(models.Model):
    CPF = models.CharField(_('CPF'), max_length=11, unique=True)
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
    numeroagencia = models.CharField(max_length=10, unique=True, default='0000000000', editable=False)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)

# gerar numero da agencia comecando no 1 e adicionando 1

    class Meta:
        verbose_name = _('Agencia')
        verbose_name_plural = _('Agencias')
        
    def __str__(self):
        return self.nomeagencia

##########################################################################################

class Conta(models.Model):
    numeroConta = models.CharField(_('Número da Conta'), primary_key=True, default=0, max_length=10, unique=True, editable=False)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    agencia = models.ForeignKey(Agencia, on_delete=models.CASCADE)
    saldo = models.DecimalField(_('Saldo'), max_digits=10, decimal_places=2, default=0, editable=False)
    dataAbertura = models.DateField(_('Data de Abertura'), auto_now_add=True)

# gerar numero da conta comecando no 1 e adicionando 1
# saldo = soma de todos as movimentacoes na conta

    class Meta:
        verbose_name = _('Conta')
        verbose_name_plural = _('Contas')

    def __str__(self):
        return f'{self.cliente.nome} - {self.saldo}'

##########################################################################################

class Transacao(models.Model):
    TIPO_TRANSACAO_CHOICES = [
        ('deposito', 'Depósito'),
        ('saque', 'Saque'),
        ('transferencia', 'Transferência'),
    ]

    STATUS_TRANSACAO_CHOICES = [
        ('concluida', 'Concluída'),
        ('cancelada', 'Cancelada'),
    ]
    
    numeroTransacao = models.CharField(_('Número da Transação'), primary_key=True, default=0, max_length=10, unique=True, editable=False)
    conta = models.ForeignKey(Conta, on_delete=models.CASCADE, related_name='transacoes')
    tipoTransacao = models.CharField(_('Tipo de Transação'), max_length=15, choices=TIPO_TRANSACAO_CHOICES)
    valor = models.DecimalField(_('Valor'), max_digits=10, decimal_places=2)
    dataHora = models.DateTimeField(_('Data e Hora'), auto_now_add=True)
    descricao = models.CharField(_('Descrição'), max_length=255, blank=True, null=True)
    status = models.CharField(_('Status'), max_length=10, choices=STATUS_TRANSACAO_CHOICES, default='Pendente', editable=False)
    contaDestino = models.ForeignKey(Conta, on_delete=models.SET_NULL, null=True, blank=True, related_name='transferencias')

# gerar numero da transacao comecando no 1 e adicionando 1
# verificar se o saldo é suficiente, 
# caso sim - status = concluida, altera o saldo e gera uma notificacao, 
# caso nao - status = cancelada, nao altera o saldo e gera uma notificacao

    class Meta:
        verbose_name = _('Transação')
        verbose_name_plural = _('Transações')
        
    def __str__(self):
        return f'{self.tipoTransacao} - {self.valor}'

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
        return f"{self.bandeira.upper()} - {self.numeroCartao}"

##########################################################################################

class Notificacao(models.Model):
    TIPO_NOTIFICACAO_CHOICES = [
        ('transacao confirmada', 'Transação confirmada'),
        ('transacao cancelada', 'Transação cancelada'),
    ]

    idNoti = models.CharField(_('ID Notificação'), primary_key=True, default=0, max_length=10, unique=True, editable=False)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, default=0)
    tipoNotificacao = models.CharField(_('Tipo de Notificação'), choices=TIPO_NOTIFICACAO_CHOICES)
    mensagem = models.TextField()
    dataEnvio = models.DateTimeField(_('Data de envio'), auto_now_add=True, editable=False)
    
# gerar id da notificacao comecando no 1 e adicionando 1
    
    class Meta:
        verbose_name = _('Notificação')
        verbose_name_plural = _('Notificações')

    def __str__(self):
        return f'{self.cliente.nome} - {self.tipoNotificacao}'