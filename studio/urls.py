from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]

# Servir arquivos de mídia em desenvolvimento e produção
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # Em produção (Render), servir arquivos de mídia através do Django
    # Isso garante que as imagens sejam acessíveis mesmo quando DEBUG=False
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
            'show_indexes': False,
        }),
    ]