from django.shortcuts import render
from core.models import Produto

def loja_home(request):
    produtos = Produto.objects.filter(ativo=True).order_by('nome')

    contexto = {
        'produtos': produtos
    }
    return render(request, 'core/loja/home.html', contexto)
