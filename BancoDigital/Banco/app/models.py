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

class Cliente(models.Model):
    nome = models.CharField(_('Nome'), max_length=100)
    CPF = models.CharField(_('CPF'), max_length=11, unique=True)
    endereco = models.CharField(_('Endereço'), max_length=200, blank=True, null=True)
    email = models.EmailField(_('E-Mail'), blank=True, null=True)
    telefone = models.CharField(_('Telefone'), max_length=15, blank=True, null=True)
    senha = models.CharField(_('Senha'), max_length=255)
    dataCadastro = models.DateTimeField( auto_now_add=True)
    foto = StdImageField(_('Foto'), null=True, blank=True, upload_to=get_file_path, variations={'thumb': {'width': 480, 'height': 480, 'crop': True}})
    
    class Meta:
        verbose_name = _('Cliente')
        verbose_name_plural = _('Clientes')

    def __str__(self):
        return self.nome



class Agencia(models.Model):
    nomeagencia = models.CharField(_('Nome da Agência'), max_length=100, null=False)
    numeroagencia = models.CharField(max_length=10, unique=True, default='0000000000', editable=False)
    endereco = models.CharField(_('Endereço da Agência'), max_length=200)

    def save(self, *args, **kwargs):
        if not self.numeroagencia or self.numeroagencia == '0000000000':
            self.numeroagencia = self.gerar_numero_agencia()
        super().save(*args, **kwargs)

    def gerar_numero_agencia(self):
        return ''.join(random.choices('0123456789', k=10))

    class Meta:
        verbose_name = _('Agencia')
        verbose_name_plural = _('Agencias')
        
    def __str__(self):
        return self.nomeagencia

    

class Conta(models.Model):
    TIPO_CONTA_CHOICES = [
        ('corrente', 'Corrente'),
        ('poupanca', 'Poupança'),
    ]

    numeroConta = models.CharField(primary_key=True, default=0, max_length=10, unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    agencia = models.ForeignKey(Agencia, on_delete=models.CASCADE)
    tipoConta = models.CharField(max_length=10, choices=TIPO_CONTA_CHOICES)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    limiteCredito = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    saldoDisponivel = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    dataAbertura = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.numeroConta == '0':
            self.numeroConta = self.gerar_numero_conta()

        self.saldoDisponivel = self.saldo + self.limiteCredito
        super().save(*args, **kwargs)

    def gerar_numero_conta(self):
        return ''.join(random.choices('0123456789', k=10))

    class Meta:
        verbose_name = _('Conta')
        verbose_name_plural = _('Contas')

    def __str__(self):
        return f'{self.cliente.nome} - {self.tipoConta}'



class Transacao(models.Model):
    TIPO_TRANSACAO_CHOICES = [
        ('deposito', 'Depósito'),
        ('saque', 'Saque'),
        ('transferencia', 'Transferência'),
        ('pagamento', 'Pagamento'),
    ]

    STATUS_TRANSACAO_CHOICES = [
        ('pendente', 'Pendente'),
        ('concluida', 'Concluída'),
        ('cancelada', 'Cancelada'),
    ]

    conta = models.ForeignKey(Conta, on_delete=models.CASCADE, related_name='transacoes')
    tipoTransacao = models.CharField(max_length=15, choices=TIPO_TRANSACAO_CHOICES)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    dataHora = models.DateTimeField(auto_now_add=True)
    dataAgendamento = models.DateTimeField(blank=True, null=True)
    descricao = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_TRANSACAO_CHOICES, default='concluida')
    contaDestino = models.ForeignKey(Conta, on_delete=models.SET_NULL, null=True, blank=True, related_name='transferencias')

    class Meta:
        verbose_name = _('Transação')
        verbose_name_plural = _('Transações')
        
    def __str__(self):
        return f'{self.tipoTransacao} - {self.valor}'



# a geração aleatoria do cartao foi feita com ajuda de IA (pra deixar claro)
class Cartao(models.Model):
    BANDEIRAS = [
        ('visa', 'Visa'),
        ('elo', 'Elo'),
        ('mastercard', 'MasterCard'),
    ]

    numeroCartao = models.BigIntegerField(unique=True, blank=True)  # Defina como blank=True para que possa ser gerado
    bandeira = models.CharField(max_length=20, choices=BANDEIRAS, default='visa')
    cvv = models.IntegerField(blank=True)  # Permita que seja gerado
    dataExpiracao = models.DateField(blank=True)  # Permita que seja gerada
    conta = models.ForeignKey(Conta, on_delete=models.CASCADE)

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



class Notificacao(models.Model):
    TIPO_NOTIFICACAO_CHOICES = [
        ('transacao', 'Transação'),
        ('seguranca', 'Segurança'),
        ('informativo', 'Informativo'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tipoNotificacao = models.CharField(max_length=15, choices=TIPO_NOTIFICACAO_CHOICES)
    mensagem = models.TextField()
    dataEnvio = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Notificação')
        verbose_name_plural = _('Notificações')

    def __str__(self):
        return f'{self.cliente.nome} - {self.tipoNotificacao}'

class Extrato(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True)
    conta = models.ForeignKey(Conta, on_delete=models.SET_NULL, null=True)
    acao = models.CharField(max_length=255)
    dataHora = models.DateTimeField(auto_now_add=True)
    detalhes = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = _('Extrato')
        verbose_name_plural = _('Extratos')

    def __str__(self):
        return f'{self.cliente.nome} - {self.acao}'
