from django.urls import path

from . import views

urlpatterns = [
    path('sf/', views.selecionar_funcionario, name='selecionar_funcionario'),
    path('sf2/', views.selecionar_funcionario2, name='selecionar_funcionario2'),
    path('gerar-pdf/<int:codigo_fc>/<int:comp>/', views.gerar_pdf_direto, name='gerar_pdf_direto'),
    path('upload/', views.upload_excel, name='upload_excel'),
]
