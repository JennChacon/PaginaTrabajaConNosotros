from django.contrib import admin
from django.forms import TextInput, Textarea
from .models import *

class Personas_PostuladaAdmin(admin.ModelAdmin):
    search_fields=('cargo__nombre','nombres','apellidos','numero_identificacion','correo','telefono','telefono_adicional','fecha_nacimiento',
    'pais_nacimiento','departamento_nacimiento','ciudad_nacimiento','genero',
    'soy_empleado','departamento_residencia','municipio_residencia','direccion','formacion_1','area_formacion_1',
    'institucion_1','formacion_2','area_formacion_2','institucion_2','formacion_3','area_formacion_3',
    'institucion_3','formacion_4','area_formacion_4','institucion_4','idioma_1','nivel_idioma_1','idioma_2',
    'nivel_idioma_2','idioma_3','nivel_idioma_3','empresa_1','cargo_1','funciones_y_logros_1','empresa_2',
    'cargo_2','funciones_y_logros_2','empresa_3','cargo_3','funciones_y_logros_3','empresa_4','cargo_4',
    'funciones_y_logros_4','empresa_5','cargo_5','funciones_y_logros_5','empresa_6','cargo_6',
    'funciones_y_logros_6','empresa_7','cargo_7','funciones_y_logros_7','empresa_8','cargo_8',
    'funciones_y_logros_8','empresa_9','cargo_9','funciones_y_logros_9','empresa_10','cargo_10',
    'funciones_y_logros_10','areas_de_interes','otras_areas_de_interes','ultimo_salario',
    'aspiracion_salarial','referido_por','comentarios')

    formfield_overrides = { 
        models.CharField: {'widget': TextInput(attrs={'size':'100'})}, 
        models.TextField: {'widget': Textarea(attrs={'rows':5, 'cols':30})}, 
    }
    ordering=("fecha_creacion",)
    list_display = ('nombres','apellidos','empresa_1','cargo_1','funciones_y_logros_1','cargo','numero_identificacion','fecha_creacion','revisado')
    list_filter = ['cargo','revisado','referido_por','genero','soy_empleado','departamento_residencia','formacion_1',
    'area_formacion_1','institucion_1','idioma_1','empresa_1','empresa_2','areas_de_interes','ultimo_salario','aspiracion_salarial']
    list_per_page = 20
    readonly_fields=('cargo','nombres','apellidos','identificacion','numero_identificacion','correo','telefono',
    'telefono_adicional','fecha_nacimiento','pais_nacimiento','departamento_nacimiento','ciudad_nacimiento','genero',
    'soy_empleado','departamento_residencia','municipio_residencia','direccion','formacion_1','area_formacion_1','tarjeta_profesional_1',
    'institucion_1','fecha_finalizacion_estudio_1','formacion_2','area_formacion_2','tarjeta_profesional_2','institucion_2',
    'fecha_finalizacion_estudio_2','formacion_3','area_formacion_3','tarjeta_profesional_3',
    'institucion_3','fecha_finalizacion_estudio_3','formacion_4','area_formacion_4','tarjeta_profesional_4','institucion_4',
    'fecha_finalizacion_estudio_4','idioma_1','nivel_idioma_1','idioma_2','nivel_idioma_2','idioma_3','nivel_idioma_3',
    'empresa_1','cargo_1','funciones_y_logros_1','fecha_finalizacion_experiencia_1','empresa_2','cargo_2','funciones_y_logros_2',
    'fecha_finalizacion_experiencia_2','empresa_3','cargo_3','funciones_y_logros_3','fecha_finalizacion_experiencia_3',
    'empresa_4','cargo_4','funciones_y_logros_4','fecha_finalizacion_experiencia_4','empresa_5',
    'cargo_5','funciones_y_logros_5','fecha_finalizacion_experiencia_5','empresa_6','cargo_6','funciones_y_logros_6',
    'fecha_finalizacion_experiencia_6','empresa_7','cargo_7','funciones_y_logros_7',
    'fecha_finalizacion_experiencia_7','empresa_8','cargo_8','funciones_y_logros_8',
    'fecha_finalizacion_experiencia_8','empresa_9','cargo_9','funciones_y_logros_9',
    'fecha_finalizacion_experiencia_9','empresa_10','cargo_10','funciones_y_logros_10',
    'fecha_finalizacion_experiencia_10','areas_de_interes',
    'otras_areas_de_interes','ultimo_salario','aspiracion_salarial','archivo_HV','fecha_creacion')


class CargoAdmin(admin.ModelAdmin):
    search_fields=('nombre','area')
    formfield_overrides = { 
        models.CharField: {'widget': TextInput(attrs={'size':'100'})}, 
        models.TextField: {'widget': Textarea(attrs={'rows':10, 'cols':100})}, 
    }

    list_display = ('nombre','area','inicio_vacante','vencimiento_vacante','habilitado')
    list_filter = ['nombre','area']
    list_per_page = 20

admin.site.register(Cargo, CargoAdmin)
admin.site.register(Personas_Postulada,Personas_PostuladaAdmin)
