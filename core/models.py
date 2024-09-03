from django.db import models

class Base(models.Model):
    criado = models.DateField('Data de Criação', auto_now_add=True)
    modificado = models.DateField('Data de Atualização',auto_now_add=True)
    ativo = models.BooleanField('Ativo?',default=True)

    class meta:
        abstract = True

class Orcamento(models.Model):
    cliente = models.CharField('Nome Cliente', max_length=80, null=False, blank = False)
    endereco = models.CharField('Endereço',max_length=50)
    servico = models.CharField('Serviço',max_length=15, null=True)
    descricao = models.TextField()
    data = models.DateField('Data',auto_now=True)
    valor = models.DecimalField(max_digits=8, decimal_places=2, null=True)


    def __str__(self):
        return self.cliente

