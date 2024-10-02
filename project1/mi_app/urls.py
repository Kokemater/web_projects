from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.main, name='main'),
    path('editor/', views.editor, name='editor'),
    path('graph_funcs/', views.graph_funcs, name='graph_funcs'),
    path('machine_learning',views.machine_learning, name='machine_learning'),
    path('recibir_texto/', views.recibir_texto, name='recibir_texto'),
    path('graficar/', views.graficar, name='graficar'),
    path('neural_network/', views.neural_network, name='neural_network'),
    path('sorting_algorithms/', views.sorting_algorithms, name = 'sorting_algorithms'),
    path('send_sorting_algorithm', views.send_sorting_algorithm, name='send_sorting_algorithm'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)