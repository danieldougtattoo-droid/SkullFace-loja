from django.contrib import admin
from .models import Artista, Trabalho, Estilo, Categoria, Produto, Cliente, Pedido, ItemPedido, Pagamento, PedidoStatus

@admin.register(Artista)
class ArtistaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ativo')
    list_filter = ('ativo',)
    search_fields = ('nome',)

@admin.register(Trabalho)
class TrabalhoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'artista', 'estilo', 'publicado', 'criado_em')
    list_filter = ('publicado', 'artista', 'estilo')
    search_fields = ('titulo',)
    list_editable = ('publicado',)

@admin.register(Estilo)
class EstiloAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ativo')
    list_filter = ('ativo',)
    search_fields = ('nome',)

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ativo')
    list_filter = ('ativo',)
    search_fields = ('nome',)

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'preco', 'ativo', 'criado_em')
    list_filter = ('ativo', 'categoria')
    search_fields = ('nome',)

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'telefone', 'email', 'criado_em')
    search_fields = ('nome', 'telefone')

class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0
    readonly_fields = ('preco_unitario',)

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_filter = ('status',)
    fields = ('cliente', 'status', 'total', 'criado_em')
    inlines = [ItemPedidoInline]
    readonly_fields = ('total', 'criado_em')

    def get_readonly_fields(self, request, obj=None):
        base = ('total', 'criado_em')

        if obj and obj.status in (PedidoStatus.PAGO, PedidoStatus.ENVIADO, PedidoStatus.FINALIZADO,):
            return base + ('status',)

        return base 

@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'metodo', 'status', 'valor', 'criado_em')
    list_filter = ('status', 'metodo')