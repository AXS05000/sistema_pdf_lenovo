from django import forms

from .models import Funcionario


class SelecionarFuncionarioForm(forms.Form):

    class Meta:
        model = Funcionario
        fields = ['matricula', 'comp']


    matricula = forms.IntegerField()
    comp = forms.IntegerField()
