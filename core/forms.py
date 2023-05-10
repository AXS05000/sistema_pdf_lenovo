from django import forms

from .models import Funcionario


class SelecionarFuncionarioForm(forms.Form):

    class Meta:
        model = Funcionario
        fields = ['codigo_fc', 'comp']


    matricula = forms.IntegerField()
    comp = forms.IntegerField()
