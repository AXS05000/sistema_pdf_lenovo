from django.db import models


class Funcionario(models.Model):
    matricula = models.IntegerField('Matricula', unique=True)
    nome = models.CharField('Nome', max_length=100)
    cargo = models.CharField('Cargo', max_length=100)
    comp = models.IntegerField('Comp')
    

    class Meta:
        ordering = ['comp', 'matricula']

    def __str__(self):
        return f'{self.comp} - {self.matricula} - {self.nome}'