# models.py
from django.db import models
from django.utils import timezone 
class user_info(models.Model):
    nome=models.CharField(max_length=50, blank=None)
    email=models.CharField(max_length=250, blank=None)
    senha=models.CharField(max_length=50, blank=None)
    tipo=models.CharField(max_length=50, default=0)
    telefone=models.IntegerField()
    cidade=models.CharField(max_length=50, blank=None)
    enctype_hash=models.CharField(editable=False, unique=True, max_length=7)

class user_complemento(models.Model):
    id_id=models.IntegerField(default=0)
    cpf=models.CharField(max_length=11, blank=True)
    date=models.CharField(max_length=10, null=True)
    cep=models.CharField(max_length=10, blank=True)
    estado=models.CharField(max_length=50, blank=True)
    endereco=models.CharField(max_length=50, blank=True)
    rua=models.CharField(max_length=50, blank=True)
    numero=models.IntegerField(blank=True)
    complemento=models.CharField(max_length=50, default='desconhecido')

class PubInfo(models.Model):
    titulo=models.CharField(max_length=10, default='IMG_SEC')
    castramento=models.CharField(default='Não', max_length=5)
    raca=models.CharField(max_length=50, default='Desconhecida')
    sexo=models.CharField(default='None', max_length=5)
    idade=models.IntegerField(default=0)
    desc=models.CharField(max_length=150, default='')
    tipo_n=models.CharField(default='Desconhecido', max_length=5)
    data_pub=models.DateTimeField(default=timezone.now, editable=None)
    creator=models.IntegerField(blank=False)
    imgpub=models.ImageField(null=True, blank=True)
    on_true=models.IntegerField(default=1)
# Create your models here.

class Fav_user(models.Model):
    id_pub = models.IntegerField()
    user_id = models.IntegerField()

class RequisicaoAdotar(models.Model):
    remetente = models.IntegerField()
    destinatario = models.IntegerField()
    pub_selec = models.IntegerField()
    msg=models.CharField(max_length=250)
    resposta=models.CharField(default='Não Respondida', max_length=25)
    log_on = models.BooleanField(default=False)