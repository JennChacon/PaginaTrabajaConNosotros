from django.urls import path
from .views import *

urlpatterns = [
    path('', home,name="home"),
    path('vacantes/<filtro>', vacantes, name="vacantes"),
    path('cargos/<idCargos>', cargos, name="cargos"),
    path('formulario/<idCargos>', formulario, name="formulario"),
    path('enviarForm/', enviarForm, name="enviarForm"),
    path('depNacim/', depNacim, name="depNacim"),
    path('ciudadNacim/', ciudadNacim, name="ciudadNacim"),
    path('ciudadResi/', ciudadResi, name="ciudadResi"),
    path('estudios/', estudios, name="estudios"),
    path('gracias/', gracias, name="gracias"),
]
