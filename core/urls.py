from django.urls import path

from . import views

urlpatterns = [
    path('sf/', views.selecionar_funcionario, name='selecionar_funcionario'),
]
