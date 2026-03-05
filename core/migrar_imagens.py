import os
import cloudinary
import cloudinary.uploader
from django.conf import settings
from core.models import Trabalho, Produto

cloudinary.config(
    cloud_name=settings.CLOUDINARY_STORAGE['CLOUD_NAME'],
    api_key=settings.CLOUDINARY_STORAGE['API_KEY'],
    api_secret=settings.CLOUDINARY_STORAGE['API_SECRET'],
)

def migrar_imagens():
    for t in Trabalho.objects.all():
        try:
            if t.imagem and os.path.exists(t.imagem.path):
                result = cloudinary.uploader.upload(t.imagem.path)
                t.imagem = result['secure_url']
                t.save()
                print("Trabalho migrado:", t.id)
            else:
                print("Arquivo não encontrado:", t.imagem)
        except Exception as e:
            print("Erro no Trabalho:", e)

    for p in Produto.objects.all():
        try:
            if p.imagem and os.path.exists(p.imagem.path):
                result = cloudinary.uploader.upload(p.imagem.path)
                p.imagem = result['secure_url']
                p.save()
                print("Produto migrado:", p.id)
            else:
                print("Arquivo não encontrado:", p.imagem)
        except Exception as e:
            print("Erro no Produto:", e)
    print("Imagens migradas com sucesso")