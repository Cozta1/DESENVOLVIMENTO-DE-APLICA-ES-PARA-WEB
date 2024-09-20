import uuid

from django.db import models
from stdimage.models import StdImageField
from django.utils.translation import gettext_lazy as _

def get_file_path(_instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return filename

# Create your models here.
from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    CPF = models.CharField(max_length=11, unique=True)
    endereco = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    senha = models.CharField(max_length=255)  # Hash da senha
    dataCadastro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Cliente')
        verbose_name_plural = _('Clientes')

    def __str__(self):
        return self.nome

class Agencia(models.Model):
    nomeAgencia = models.CharField(max_length=100)
    endereco = models.CharField(max_length=200)

    class Meta:
        verbose_name = _('Agencia')
        verbose_name_plural = _('Agencias')
        
    def __str__(self):
        return self.nomeAgencia

class Conta(models.Model):
    TIPO_CONTA_CHOICES = [
        ('corrente', 'Corrente'),
        ('poupanca', 'Poupança'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    agencia = models.ForeignKey(Agencia, on_delete=models.CASCADE)
    tipoConta = models.CharField(max_length=10, choices=TIPO_CONTA_CHOICES)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    limiteCredito = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    saldoDisponivel = models.DecimalField(max_digits=10, decimal_places=2)
    dataAbertura = models.DateField()
    
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

class Cartao(models.Model):
    conta = models.ForeignKey(Conta, on_delete=models.CASCADE)
    dataExpiracao = models.DateField()
    cvv = models.IntegerField()
    
    class Meta:
        verbose_name = _('Cartão')
        verbose_name_plural = _('Cartões')

    def __str__(self):
        return f'{self.conta.cliente.nome} - {self.dataExpiracao}'

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

