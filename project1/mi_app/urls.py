from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.main, name='main'),
    path('editor/', views.editor, name='editor'),
    path('recibir_texto/', views.recibir_texto, name='recibir_texto'),
    path('graficar/', views.graficar, name='graficar'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)