from django.shortcuts import render
from .models import Trabalho, Estilo, Produto

def home(request):
    # Buscar trabalhos de tatuagem (excluindo piercing)
    trabalhos_tatuagem = Trabalho.objects.filter(
        publicado=True
    ).exclude(
        artista__nome__icontains='ester'
    ).order_by('-id')
    
    # Buscar trabalhos de piercing (Ester)
    trabalhos_piercing = Trabalho.objects.filter(
        publicado=True,
        artista__nome__icontains='ester'
    ).order_by('-id')
     
    # Buscar produtos ativos para a loja
    produtos = Produto.objects.filter(ativo=True).order_by('nome')
    
    context = {
        'trabalhos_tatuagem': trabalhos_tatuagem,
        'trabalhos_piercing': trabalhos_piercing,
        'produtos': produtos,
    }
    return render(request, 'core/home.html', context)


def galeria(request):
    estilos = Estilo.objects.all()
    estilo_id = request.GET.get('estilo')

    estilo_selecionado = None
    trabalhos = Trabalho.objects.none()

    if estilo_id:
        try:
            estilo_selecionado = Estilo.objects.get(id=estilo_id)
            trabalhos = Trabalho.objects.filter(publicado=True, estilo=estilo_selecionado)
        except Estilo.DoesNotExist:
            estilo_selecionado = None
            trabalhos = Trabalho.objects.none()

    return render(request, 'core/galeria.html', {
        'estilos': estilos,
        'trabalhos': trabalhos,
        'estilo_selecionado': estilo_selecionado
    })

def sobre(request):
    return render(request, 'core/sobre.html')

def estúdio(request):
    return render(request, 'core/estudio.html')

def artistas(request):
    return render(request, 'core/artistas.html')

def artista_detalhe(request, slug):
    artistas = {
        'doug': {
            'nome': 'Doug Tattoo',
            'bio': 'Doug Tattoo é um artista de 26 anos de experiência, com especialidade em desenvolver tatuagens incriveis com linhas precisas e detalhes. Ele é conhecido por suas tatuagens com contrastes vibrantes, que refletem sua paixão pela arte e pela cultura da tattoo.',
            'estilos': ['Realism', 'blackwork','neotradicional','tribal','entre outros'],
            'foto': 'core/img/artista1.jpg',
            'instagram': 'https://www.instagram.com/dougtattoo/',
            'galeria_url': "/galeria?tipo=tatuagem"
        },
        'ester': {
            'nome': 'Ester Piercing',
            'bio': 'Ester Piercing é uma artista, com especialidade em aplicações seguras, usando a anatomia como base.',
            'estilos': ['Especialista em todas aplicações e bio-segurança'],
            'foto': 'core/img/artista2.jpg',
            'instagram': 'https://www.instagram.com/ester.piercer/',
            'galeria_url': "/galeria?tipo=piercing"
        }
    }
    
    artista = artistas.get(slug)
    if not artista:
        return render(request, 'core/404.html')
    
    return render(request, 'core/artista_detalhe.html', {'artista': artista})


def contato(request):
    return render(request, 'core/contato.html')

def loja_home(request):
    produtos = Produto.objects.filter(ativo=True)
    return render(request, 'core/loja/home.html', {'produtos': produtos})
    
   