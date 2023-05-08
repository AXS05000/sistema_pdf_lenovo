from django.shortcuts import render

from .forms import SelecionarFuncionarioForm
from .models import Funcionario
from .utils import gerar_pdf, importar_excel


def selecionar_funcionario(request):
    if request.method == 'POST':
        form = SelecionarFuncionarioForm(request.POST)
        if form.is_valid():
            matricula = form.cleaned_data['matricula']
            comp = form.cleaned_data['comp']
            try:
                funcionario = Funcionario.objects.get(matricula=matricula, comp=comp)
            
                return gerar_pdf(funcionario)
            except Funcionario.DoesNotExist:
                form.add_error(None, 'Funcionário não encontrado para a matrícula e competência informadas.')
    else:
        form = SelecionarFuncionarioForm()

    return render(request, 'pdf/selecionar_funcionario.html', {'form': form})