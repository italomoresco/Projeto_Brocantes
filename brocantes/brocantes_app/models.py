from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class MyUserManager(BaseUserManager):
    def create_user(self, login, password=None, **extra_fields):
        if not login:
            raise ValueError('The Login field must be set')
        user = self.model(login=login, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(login, password, **extra_fields)

class User(AbstractBaseUser):
    name = models.CharField(max_length=100)
    login = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False) 

    objects = MyUserManager()

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.login

class Estado(models.Model):
    nome = models.CharField(max_length=100)
    sigla = models.CharField(max_length=2)  

    def __str__(self):
        return self.nome

class Cidade(models.Model):
    nome = models.CharField(max_length=100)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, related_name='cidades')

    def __str__(self):
        return self.nome

class Instituicao(models.Model):
    codigo = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    estado = models.ForeignKey(Estado, on_delete=models.PROTECT)
    cidade = models.ForeignKey(Cidade, on_delete=models.PROTECT)

    def __str__(self):
        return self.nome

class Doador(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome", null=False, blank=False)
    email = models.EmailField(max_length=100, verbose_name="Email", null=True, blank=True)
    telefone = models.CharField(max_length=20, verbose_name="Telefone", null=True, blank=True)
    documento_id = models.CharField(max_length=50, verbose_name="Documento de Identificação", null=True, blank=True)
    cidade = models.ForeignKey('Cidade', on_delete=models.CASCADE, verbose_name="Cidade")
    estado = models.ForeignKey('Estado', on_delete=models.CASCADE, verbose_name="Estado")

    def __str__(self):
        return self.nome

class Doacao(models.Model):
    doador = models.ForeignKey(Doador, on_delete=models.CASCADE)
    numero_controle = models.CharField(max_length=30)
    link_documento_original = models.CharField(max_length=200)
    link_documento_tajado = models.CharField(max_length=200)
    descricao_arquivo = models.CharField(max_length=200)
    ano = models.IntegerField()
    paginas = models.IntegerField()
    largura = models.FloatField()
    comprimento = models.FloatField()
    classificacao = models.CharField(max_length=50)
    nivel = models.CharField(max_length=50)
    curso = models.CharField(max_length=50)
    instituicao = models.ForeignKey(Instituicao, on_delete=models.CASCADE)
    cidade = models.ForeignKey(Cidade, on_delete=models.CASCADE)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    observacao = models.CharField(max_length=300, blank=True, null=True)
    digitalizado = models.BooleanField(default=False)
    devolucao = models.BooleanField(default=False)
    recebido = models.CharField(max_length=20, blank=True, null=True)
    publicado = models.BooleanField(default=False)

    def __str__(self):
        return f"Doação {self.numero_controle}"

