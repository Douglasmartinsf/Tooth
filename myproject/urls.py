#from django.contrib import admin
#from django.urls import path, include
#from django.shortcuts import redirect
#from django.conf import settings
#from django.conf.urls.static import static
#
#urlpatterns = [
#    path('', lambda request: redirect('upload')),  # redireciona para a view “upload”
##nginx    path('imagemproc/', include('imagemproc.urls')),
#    path('', include('imagemproc.urls')),
#]
#
## servir arquivos de media em modo debug
#if settings.DEBUG:
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('imagemproc.urls')),
]

# Adicionar rota de desenvolvimento apenas quando DEBUG=True
if settings.DEBUG:
    from imagemproc.dev_views import dev_login
    urlpatterns.append(path('dev-login/', dev_login, name='dev_login'))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

