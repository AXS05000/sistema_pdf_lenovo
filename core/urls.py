from django.urls import path

from . import views

urlpatterns = [
    path('sf/', views.selecionar_funcionario, name='selecionar_funcionario'),
    path('gerar-pdf/<int:matricula>/<int:comp>/', views.gerar_pdf_direto, name='gerar_pdf_direto'),
    path('upload/', views.upload_excel, name='upload_excel'),
]
