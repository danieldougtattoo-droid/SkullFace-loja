from cloudinary.models import CloudinaryField
from django.db import models
from django.db.models import Sum, F
from PIL import Image
import os
from django.core.files.base import ContentFile
from io import BytesIO

class Artista(models.Model):
    nome = models.CharField(max_length=100)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

class Estilo(models.Model):
    nome = models.CharField(max_length=100)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

class Trabalho(models.Model):
    titulo = models.CharField(max_length=200)
    artista = models.ForeignKey(Artista, on_delete=models.CASCADE)
    estilo = models.ForeignKey(Estilo, on_delete=models.SET_NULL, null=True, blank=True)
    imagem = CloudinaryField('image')
    publicado = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    destaque = models.BooleanField(default=False)

    def __str__(self):
        return self.titulo

        #Loja Online

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

        #Produtos piercings
class Produto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='produtos')
    nome = models.CharField(max_length=120)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    imagem = CloudinaryField('image')
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome
    
    def save(self, *args, **kwargs):
        # Verificar se é uma nova imagem ou se a imagem foi alterada
        imagem_alterada = False
        if self.pk:
            try:
                old_instance = Produto.objects.get(pk=self.pk)
                imagem_alterada = old_instance.imagem != self.imagem
            except Produto.DoesNotExist:
                imagem_alterada = bool(self.imagem)
        else:
            imagem_alterada = bool(self.imagem)
        
        # Processar imagem apenas se for nova ou alterada
        if imagem_alterada and self.imagem:
            try:
                # Abrir a imagem original
                img = Image.open(self.imagem)
                
                # Converter para RGB se necessário (para JPEG)
                if img.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', img.size, (0, 0, 0))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Otimizar imagem mantendo tamanho original
                # Apenas reduzir qualidade para diminuir tamanho do arquivo
                # O CSS já limita o tamanho visual no grid
                output = BytesIO()
                img.save(output, format='JPEG', quality=85, optimize=True)
                output.seek(0)
                
                # Substituir o arquivo original
                nome_arquivo = os.path.basename(self.imagem.name)
                self.imagem.save(
                    nome_arquivo,
                    ContentFile(output.read()),
                    save=False
                )
                output.close()
            except Exception:
                # Se houver erro no processamento, continuar normalmente
                pass
        
        super().save(*args, **kwargs)

        #Cliente (Desacoplado do user)
class Cliente(models.Model):
    nome = models.CharField(max_length=120)
    telefone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

        #Pedido (Relacionado ao cliente)
class PedidoStatus(models.TextChoices):
    CRIADO = "CRIADO", "Criado"
    AGUARDANDO_PAGAMENTO = "AGUARDANDO_PAGAMENTO", "Aguardando Pagamento"
    PAGO = "PAGO", "Pago"
    ENVIADO = "ENVIADO", "Enviado"
    FINALIZADO = "FINALIZADO", "Finalizado"
    CANCELADO = "CANCELADO", "Cancelado"

class Pedido(models.Model):
    STATUS_CHOICES = [
        ("CRIADO", "Criado"),
        ("AGUARDANDO_PAGAMENTO", "Aguardando Pagamento"),
        ("PAGO", "Pago"),
        ("CANCELADO", "Cancelado"),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='pedidos')
    status = models.CharField(max_length=30, choices=PedidoStatus.choices, default=PedidoStatus.CRIADO)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente.nome}"

    def recalcular_total(self):
        total = self.itens.aggregate(total=Sum(F('quantidade') * F('preco_unitario')))['total'] or 0
        self.total = total
        self.save(update_fields=['total'])
    
        #Item do pedido (Relacionado ao pedido)
class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.IntegerField(default=1)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        if not self.preco_unitario:
            self.preco_unitario = self.produto.preco
        super().save(*args, **kwargs)
        self.pedido.recalcular_total()

        #Pagamento abstração

class Pagamento(models.Model):
    METODO_CHOICES = [
        ("WHATSAPP", "Whatsapp"),
        ("PIX", "Pix"),
        ("CARTAO", "Cartão"),
    ]

    STATUS_CHOICES = [
        ("PENDENTE", "Pendente"),
        ("CONFIRMADO", "Confirmado"),
        ("CANCELADO", "Cancelado"),
    ]

    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE, related_name='pagamento')
    metodo = models.CharField(max_length=20, choices=METODO_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDENTE")
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pagamento #{self.pedido.id}"