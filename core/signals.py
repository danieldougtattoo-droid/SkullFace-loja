from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from django.db.models import Sum, F

from .models import ItemPedido, Pedido

def recalcular_total(pedido):
    total = pedido.itens.aggregate(total=Sum(F('preco_unitario') * F('quantidade')))['total'] or 0

    pedido.total = total
    pedido.save(update_fields=['total'])

@receiver(post_save, sender=ItemPedido)
def atualizar_total_apos_salvar_item(sender, instance, **kwargs):
    recalcular_total(instance.pedido)