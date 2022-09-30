from django.shortcuts import render
from django.http import JsonResponse
import json
from . models import *
import datetime
from django.core.mail import send_mail
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from django.conf import settings
from App.models import Cargo
from django.core.mail import EmailMessage
import requests
import os
import codecs
from datetime import datetime
from django.core.files.storage import FileSystemStorage
import time
import mimetypes
import logging
import logging.handlers as handlers
import socket

def home(request):
    '''
    img=Image.objects.all()  
    context={'img':img}
    '''
    return render(request, 'App/home.html', {})

def gracias(request):
    context={}
    return render(request, 'App/gracias.html', context)

def vacantes(request, filtro):
    cargos=Cargo.objects.all()
    
    if filtro=='1':
        cargos=cargos.order_by('nombre')
    elif filtro=='2':
        cargos=cargos.order_by('-nombre')
    
    fechaActual=datetime.now().date
    
    context={'cargos': cargos, 'fechaActual':fechaActual}

    return render(request, 'App/vacantes.html', context)
    
def cargos(request, idCargos):
    cargos=Cargo.objects.get(id=idCargos)  
    splitObjetivo=cargos.objetivo.split("*")
    splitContrato=cargos.contrato.split("*")
    splitFormacion=cargos.formacion.split("*")
    splitResponsabilidades=cargos.responsabilidades.split("*")
    splitExperiencia=cargos.experiencia.split("*")
    splitIdiomas=cargos.idiomas.split("*")
    splitJornada=cargos.jornada.split("*")
    splitUbicacion=cargos.ubicacion.split("*")
    splitConocimientos=cargos.conocimientos.split("*")
    splitSistemasPH=cargos.sistemas_programas_herramientas.split("*")
    context={'cargos': cargos,'splitResponsabilidades':splitResponsabilidades,'splitJornada':splitJornada,
    'splitSistemasPH':splitSistemasPH,'splitObjetivo':splitObjetivo,'splitFormacion':splitFormacion,
    'splitExperiencia':splitExperiencia,'splitIdiomas':splitIdiomas,'splitUbicacion':splitUbicacion,
    'splitConocimientos':splitConocimientos,'splitContrato':splitContrato}
    return render(request, 'App/cargos.html', context)


def generate_decoded(url):
    with open(url,'r',encoding='utf-8') as archivo:
        datos=archivo.read()

    objeto=json.loads(datos)
    return objeto

def depNacim(request):
    pais = request.GET.get('paisNac')
    resultPais = generate_decoded('App/paises.json')
    resultDepart= generate_decoded('App/departamentos.json')

    context={'resultDepart':resultDepart,'resultPais':resultPais,'pais':pais}

    return render(request, 'App/depNacim.html', context)    

def ciudadNacim(request):
    depNacim = request.GET.get('depNacim')
    resultDepart= generate_decoded('App/departamentos.json')
    resultCiudades = generate_decoded('App/ciudades.json')

    context={'resultDepart':resultDepart,'resultCiudades':resultCiudades,'depNacim':depNacim}

    return render(request, 'App/ciudadNacim.html', context)       

def ciudadResi(request):
    depResi = request.GET.get('depResi')
    resultDepart= generate_decoded('App/departamentos.json')
    resultCiudades=generate_decoded('App/ciudades.json')

    context={'resultDepart':resultDepart,'resultCiudades':resultCiudades,'depResi':depResi}

    return render(request, 'App/ciudadResi.html', context)

def estudios(request):
    formacion = str(request.GET.get('formacion'))
    areas={
        "Administración":"Administración",
        "Agronomía":"Agronomía",
        "Antropología, Artes Liberales":"Antropología, Artes Liberales",
        "Arquitectura y afines":"Arquitectura y afines",
        "Artes Plásticas, Visuales y afines":"Artes Plásticas, Visuales y afines",
        "Artes Representativas":"Artes Representativas",
        "Bacteriología":"Bacteriología",
        "Bibliotecología, otros de Ciencias Sociales y Humanas":"Bibliotecología, otros de Ciencias Sociales y Humanas",
        "Biología, Microbiología y afines":"Biología, Microbiología y afines",
        "Ciencia Política, Relaciones Internacionales":"Ciencia Política, Relaciones Internacionales",
        "Comunicación Social, Periodismo y afines":"Comunicación Social, Periodismo y afines",
        "Contaduría Pública":"Contaduría Pública",
        "Deportes, Educación Física y Recreación":"Deportes, Educación Física y Recreación",
        "Derecho y afines":"Derecho y afines",
        "Diseño":"Diseño",
        "Economía":"Economía",
        "Educación":"Educación",
        "Enfermería":"Enfermería",
        "Filosofía, Teología y afines":"Filosofía, Teología y afines",
        "Física":"Física",
        "Formación relacionada con el campo militar o policial":"Formación relacionada con el campo militar o policial",
        "Geografía, Historia":"Geografía, Historia",
        "Geología, otros programas de Ciencias Naturales":"Geología, otros programas de Ciencias Naturales",
        "Ingeniería Administrativa y afines":"Ingeniería Administrativa y afines",
        "Ingeniería Agrícola, Forestal y afines":"Ingeniería Agrícola, Forestal y afines",
        "Ingeniería Agroindustrial, Alimentos y afines":"Ingeniería Agroindustrial, Alimentos y afines",
        "Ingeniería Agrónoma, Pecuaria y afines":"Ingeniería Agrónoma, Pecuaria y afines",
        "Ingeniería Ambiental, Sanitaria y afines":"Ingeniería Ambiental, Sanitaria y afines",
        "Ingeniería Biomédica y afines":"Ingeniería Biomédica y afines",
        "Ingeniería Civil y afines":"Ingeniería Civil y afines",
        "Ingeniería de Minas, Metalurgia y afines":"Ingeniería de Minas, Metalurgia y afines",
        "Ingeniería de Sistemas, Telemática y afines":"Ingeniería de Sistemas, Telemática y afines",
        "Ingeniería Eléctrica y afines":"Ingeniería Eléctrica y afines",
        "Ingeniería Electrónica, Telecomunicaciones y afines":"Ingeniería Electrónica, Telecomunicaciones y afines",
        "Ingeniería Industrial y afines":"Ingeniería Industrial y afines",
        "Ingeniería Mecánica y afines":"Ingeniería Mecánica y afines",
        "Ingeniería Química y afines":"Ingeniería Química y afines",
        "Instrumentación Quirúrgica":"Instrumentación Quirúrgica",
        "Lenguas Modernas, Literatura, Lingüística y afines":"Lenguas Modernas, Literatura, Lingüística y afines",
        "Matemáticas, Estadística y afines":"Matemáticas, Estadística y afines",
        "Medicina":"Medicina",
        "Medicina Veterinaria":"Medicina Veterinaria",
        "Música":"Música",
        "Nutrición y Dietética":"Nutrición y Dietética",
        "Odontología":"Odontología",
        "Optometría, otros programas de Ciencias de la Salud":"Optometría, otros programas de Ciencias de la Salud",
        "Otras Ingenierías":"Otras Ingenierías",
        "Otros programas asociados a Bellas Artes":"Otros programas asociados a Bellas Artes",
        "Psicología":"Psicología",
        "Publicidad y afines":"Publicidad y afines",
        "Química y afinas":"Química y afinas",
        "Salud Pública":"Salud Pública",
        "Sociología, Trabajo Social y afines":"Sociología, Trabajo Social y afines",
        "Terapias":"Terapias",
        "Zootecnia":"Zootecnia",
    }
    areaEst=[]
    if formacion=="Preescolar":
        areaEst.append("Preescolar")
    else:
        if formacion=="Básica_Primaria_(1_-_5)":
            areaEst.append("Básica Primaria (1° - 5°)")
        else:
            if formacion=="Básica_Secundaria_(6_-_9)":
                areaEst.append("Básica Secundaria (6° - 9°)")
            else:
                if formacion=="Media_(10_-_13)":
                    areaEst.append("Bachillerato Académico")
                    areaEst.append("Bachillerato Comercial")
                    areaEst.append("Bachillerato Técnico")
                else:
                    areaEst=areas

    context={'areaEst':areaEst}

    return render(request, 'App/estudios.html', context)

def formulario(request, idCargos):

    dias={
        '01':'01',
        '02':'02',
        '03':'03',
        '04':'04',
        '05':'05',
        '06':'06',
        '07':'07',
        '08':'08',
        '09':'09',
        '10':'10',
        '11':'11',
        '12':'12',
        '13':'13',
        '14':'14',
        '15':'15',
        '16':'16',
        '17':'17',
        '18':'18',
        '19':'19',
        '20':'20',
        '21':'21',
        '22':'22',
        '23':'23',
        '24':'24',
        '25':'25',
        '26':'26',
        '27':'27',
        '28':'28',
        '29':'29',
        '30':'30',
        '31':'31'
    }

    meses=[
        {'id':"01","mes":'Enero'},
        {'id':"02","mes":'Febrero'},
        {'id':"03","mes":'Marzo'},
        {'id':"04","mes":'Abril'},
        {'id':"05","mes":'Mayo'},
        {'id':"06","mes":'Junio'},
        {'id':"07","mes":'Julio'},
        {'id':"08","mes":'Agosto'},
        {'id':"09","mes":'Septiembre'},
        {'id':"10","mes":'Octubre'},
        {'id':"11","mes":'Noviembre'},
        {'id':"12","mes":'Diciembre'},
    ]

    anioMenor=1950
    anioActual=datetime.now().year
    anios=[]
    while anioMenor<=anioActual:
        anios.append(anioMenor)
        anioMenor = anioMenor+1

    documento={
        'Tarjeta identidad': 'Tarjeta identidad',
        'Cédula': 'Cédula',  
        'Cédula extranjera':'Cédula extranjera',        
        'Registro civil':'Registro civil',
        'Permiso especial de permanencia':'Permiso especial de permanencia'
    }
    formacion={
        'Preescolar':'Preescolar',
        'Básica_Primaria_(1_-_5)':'Básica Primaria (1° - 5°)',
        'Básica_Secundaria_(6_-_9)':'Básica Secundaria (6° - 9°)',
        'Media_(10_-_13)':'Media (10° - 13°)',
        'Técnico_Laboral':'Técnico Laboral',
        'Formación_Tec_profesional':'Formación Tec profesional',
        'Tecnológica':'Tecnológica',
        'Universitaria':"Universitaria",
        'Especialización':'Especialización',
        'Maestría':'Maestría',
        'Doctorado':'Doctorado'     
    }
    resultDepart = generate_decoded('App/departamentos.json')
    resultPais = generate_decoded('App/paises.json')
    idiomas={
        'Afar':'Afar',
        'Abjaso':'Abjaso',
        'Afrikaans':'Afrikaans',
        'Aimara':'Aimara',
        'Akano':'Akano',
        'Albanés':'Albanés',
        'Alemán':'Alemán',
        'Amárico':'Amárico',
        'Árabe':'Árabe',
        'Aragonés':'Aragonés',
        'Armenio':'Armenio',
        'Asamés':'Asamés',
        'Avar':'Avar',
        'Avéstico':'Avéstico',
        'Azerí':'Azerí',
        'Bambara':'Bambara',
        'Baskir':'Baskir',
        'Bengalí':'Bengalí',
        'Bhojpurí':'Bhojpurí',
        'Bielorruso':'Bielorruso',
        'Birmano':'Birmano',
        'Bislama':'Bislama',
        'Bosnio':'Bosnio',
        'Bretón':'Bretón',
        'Búlgaro':'Búlgaro',
        'Cachemiro':'Cachemiro',
        'Camboyano':'Camboyano',
        'Canarés':'Canarés',
        'Catalán':'Catalán',
        'Chamorro':'Chamorro',
        'Checheno':'Checheno',
        'Checo':'Checo',
        'Chichewa':'Chichewa',
        'Chino':'Chino',
        'Chuan':'Chuan',
        'Chuvasio':'Chuvasio',
        'Cingalés':'Cingalés',
        'Coreano':'Coreano',
        'Córnico':'Córnico',
        'Corso':'Corso',
        'Cree':'Cree',
        'Croata':'Croata',
        'Danés':'Danés',
        'Dzongkha':'Dzongkha',
        'Eslavo eclesiástico antiguo':'Eslavo eclesiástico antiguo',
        'Eslovaco':'Eslovaco',
        'Esloveno':'Esloveno',
        'Español':'Español',
        'Esperanto':'Esperanto',
        'Estonio':'Estonio',
        'Ewe':'Ewe',
        'Feroés':'Feroés',
        'Fijiano':'Fijiano',
        'Finés':'Finés',
        'Francés':'Francés',
        'Frisón':'Frisón',
        'Fula':'Fula',
        'Gaélico escocés':'Gaélico escocés',
        'Galés':'Galés',
        'Gallego':'Gallego',
        'Georgiano':'Georgiano',
        'Griego':'Griego',
        'Groenlandés':'Groenlandés',
        'Guaraní':'Guaraní',
        'Guyaratí':'Guyaratí',
        'Haitiano':'Haitiano',
        'Hausa':'Hausa',
        'Hebreo':'Hebreo',
        'Herero':'Herero',
        'Hindi':'Hindi',
        'Hiri motu':'Hiri motu',
        'Húngaro':'Húngaro',
        'Ido':'Ido',
        'Igbo':'Igbo',
        'Indonesio':'Indonesio',
        'Inglés':'Inglés',
        'Interlingua':'Interlingua',
        'Inuktitut':'Inuktitut',
        'Inupiaq':'Inupiaq',
        'Irlandés':'Irlandés',
        'Islandés':'Islandés',
        'Italiano':'Italiano',
        'Japonés':'Japonés',
        'Javanés':'Javanés',
        'Kanuri':'Kanuri',
        'Kazajo':'Kazajo',
        'Kikuyu':'Kikuyu',
        'Kirguís':'Kirguís',
        'Kirundi':'Kirundi',
        'Komi':'Komi',
        'Kongo':'Kongo',
        'Kuanyama':'Kuanyama',
        'Kurdo':'Kurdo',
        'Lao':'Lao',
        'Latín':'Latín',
        'Letón':'Letón',
        'Limburgués':'Limburgués',
        'Lingala':'Lingala',
        'Lituano':'Lituano',
        'Luba-katanga':'Luba-katanga',
        'Luganda':'Luganda',
        'Luxemburgués':'Luxemburgués',
        'Macedonio':'Macedonio',
        'Malayalam':'Malayalam',
        'Malayo':'Malayo',
        'Maldivo':'Maldivo',
        'Malgache':'Malgache',
        'Maltés':'Maltés',
        'Manés':'Manés',
        'Maorí':'Maorí',
        'Maratí':'Maratí',
        'Marshalés':'Marshalés',
        'Moldavo':'Moldavo',
        'Mongol':'Mongol',
        'Nauruano':'Nauruano',
        'Navajo':'Navajo',
        'Ndebele del norte':'Ndebele del norte',
        'Ndebele del sur':'Ndebele del sur',
        'Ndonga':'Ndonga',
        'Neerlandés':'Neerlandés',
        'Nepalí':'Nepalí',
        'Noruego':'Noruego',
        'Noruego bokmål':'Noruego bokmål',
        'Nynorsk':'Nynorsk',
        'Occidental':'Occidental',
        'Occitano':'Occitano',
        'Ojibwa':'Ojibwa',
        'Oriya':'Oriya',
        'Oromo':'Oromo',
        'Osético':'Osético',
        'Pali':'Pali',
        'Panyabí':'Panyabí',
        'Pastú':'Pastú',
        'Persa':'Persa',
        'Polaco':'Polaco',
        'Portugués':'Portugués',
        'Quechua':'Quechua',
        'Retorrománico':'Retorrománico',
        'Ruandés':'Ruandés',
        'Rumano':'Rumano',
        'Ruso':'Ruso',
        'Sami septentrional':'Sami septentrional',
        'Samoano':'Samoano',
        'Sango':'Sango',
        'Sánscrito':'Sánscrito',
        'Sardo':'Sardo',
        'Serbio':'Serbio',
        'Sesotho':'Sesotho',
        'Setsuana':'Setsuana',
        'Shona':'Shona',
        'Sindhi':'Sindhi',
        'Somalí':'Somalí',
        'Suajili':'Suajili',
        'Suazi':'Suazi',
        'Sueco':'Sueco',
        'Sundanés':'Sundanés',
        'Tagalo':'Tagalo',
        'Tahitiano':'Tahitiano',
        'Tailandés':'Tailandés',
        'Tamil':'Tamil',
        'Tártaro':'Tártaro',
        'Tayiko':'Tayiko',
        'Telugú':'Telugú',
        'Tibetano':'Tibetano',
        'Tigriña':'Tigriña',
        'Tongano':'Tongano',
        'Tsonga':'Tsonga',
        'Turco':'Turco',
        'Turcomano':'Turcomano',
        'Twi':'Twi',
        'Ucraniano':'Ucraniano',
        'Uigur':'Uigur',
        'Urdu':'Urdu',
        'Uzbeko':'Uzbeko',
        'Valón':'Valón',
        'Vascuence':'Vascuence',
        'Venda':'Venda',
        'Vietnamita':'Vietnamita',
        'Volapük':'Volapük',
        'Wolof':'Wolof',
        'Xhosa':'Xhosa',
        'Yi de Sichuán':'Yi de Sichuán',
        'Yídish':'Yídish',
        'Yoruba':'Yoruba',
        'Zulú':'Zulú',

    }

    idi=""
    for i in idiomas:
        idi = idi + "<option value=\""+i+"\">"+i+"</option>" +"*"

    formac=""
    for i in formacion:
        formac = formac + "<option value=\""+i+"\">"+formacion[i]+"</option>" +"*"

    area={
        "Administración":"Administración",
        "Agronomía":"Agronomía",
        "Antropología, Artes Liberales":"Antropología, Artes Liberales",
        "Arquitectura y afines":"Arquitectura y afines",
        "Artes Plásticas, Visuales y afines":"Artes Plásticas, Visuales y afines",
        "Artes Representativas":"Artes Representativas",
        "Bacteriología":"Bacteriología",
        "Bibliotecología, otros de Ciencias Sociales y Humanas":"Bibliotecología, otros de Ciencias Sociales y Humanas",
        "Biología, Microbiología y afines":"Biología, Microbiología y afines",
        "Ciencia Política, Relaciones Internacionales":"Ciencia Política, Relaciones Internacionales",
        "Comunicación Social, Periodismo y afines":"Comunicación Social, Periodismo y afines",
        "Contaduría Pública":"Contaduría Pública",
        "Deportes, Educación Física y Recreación":"Deportes, Educación Física y Recreación",
        "Derecho y afines":"Derecho y afines",
        "Diseño":"Diseño",
        "Economía":"Economía",
        "Educación":"Educación",
        "Enfermería":"Enfermería",
        "Filosofía, Teología y afines":"Filosofía, Teología y afines",
        "Física":"Física",
        "Formación relacionada con el campo militar o policial":"Formación relacionada con el campo militar o policial",
        "Geografía, Historia":"Geografía, Historia",
        "Geología, otros programas de Ciencias Naturales":"Geología, otros programas de Ciencias Naturales",
        "Ingeniería Administrativa y afines":"Ingeniería Administrativa y afines",
        "Ingeniería Agrícola, Forestal y afines":"Ingeniería Agrícola, Forestal y afines",
        "Ingeniería Agroindustrial, Alimentos y afines":"Ingeniería Agroindustrial, Alimentos y afines",
        "Ingeniería Agrónoma, Pecuaria y afines":"Ingeniería Agrónoma, Pecuaria y afines",
        "Ingeniería Ambiental, Sanitaria y afines":"Ingeniería Ambiental, Sanitaria y afines",
        "Ingeniería Biomédica y afines":"Ingeniería Biomédica y afines",
        "Ingeniería Civil y afines":"Ingeniería Civil y afines",
        "Ingeniería de Minas, Metalurgia y afines":"Ingeniería de Minas, Metalurgia y afines",
        "Ingeniería de Sistemas, Telemática y afines":"Ingeniería de Sistemas, Telemática y afines",
        "Ingeniería Eléctrica y afines":"Ingeniería Eléctrica y afines",
        "Ingeniería Electrónica, Telecomunicaciones y afines":"Ingeniería Electrónica, Telecomunicaciones y afines",
        "Ingeniería Industrial y afines":"Ingeniería Industrial y afines",
        "Ingeniería Mecánica y afines":"Ingeniería Mecánica y afines",
        "Ingeniería Química y afines":"Ingeniería Química y afines",
        "Instrumentación Quirúrgica":"Instrumentación Quirúrgica",
        "Lenguas Modernas, Literatura, Lingüística y afines":"Lenguas Modernas, Literatura, Lingüística y afines",
        "Matemáticas, Estadística y afines":"Matemáticas, Estadística y afines",
        "Medicina":"Medicina",
        "Medicina Veterinaria":"Medicina Veterinaria",
        "Música":"Música",
        "Nutrición y Dietética":"Nutrición y Dietética",
        "Odontología":"Odontología",
        "Optometría, otros programas de Ciencias de la Salud":"Optometría, otros programas de Ciencias de la Salud",
        "Otras Ingenierías":"Otras Ingenierías",
        "Otros programas asociados a Bellas Artes":"Otros programas asociados a Bellas Artes",
        "Psicología":"Psicología",
        "Publicidad y afines":"Publicidad y afines",
        "Química y afinas":"Química y afinas",
        "Salud Pública":"Salud Pública",
        "Sociología, Trabajo Social y afines":"Sociología, Trabajo Social y afines",
        "Terapias":"Terapias",
        "Zootecnia":"Zootecnia",
    }
    areaInteres={
        "Mercadeo y publicidad":"Mercadeo y publicidad",
        "Obra":"Obra",
        "Operaciones y procesos":"Operaciones y procesos",
        "Organización y métodos":"Organización y métodos",
        "Producción":"Producción",
        "Proyectos (análisis, desarrollo, gestión y afines)":"Proyectos (análisis, desarrollo, gestión y afines)",
        "Recepción":"Recepción",
        "Recursos Humanos y Admon. de Personal":"Recursos Humanos y Admon. de Personal",
        "Redacción y Generación de Contenido":"Redacción y Generación de Contenido",
        "Salud":"Salud",
        "Secretariado":"Secretariado",
        "Seguridad Industrial, Ambiental y Ocupacional":"Seguridad Industrial, Ambiental y Ocupacional",
        "Servicio al Cliente":"Servicio al Cliente",
        "Servicios Generales, Aseo y Vigilancia":"Servicios Generales, Aseo y Vigilancia",
        "Sistemas":"Sistemas",
        "Sistemas y tecnología":"Sistemas y tecnología",
        "Telemercadeo":"Telemercadeo",
        "Ventas":"Ventas",
        "Facturación":"Facturación",
        "Financiera: crédito y tesorería":"Financiera: crédito y tesorería",
        "Gerencia General (cargos corporativos)":"Gerencia General (cargos corporativos)",
        "Instalación y Reparaciones técnicas":"Instalación y Reparaciones técnicas",
        "Interventoría":"Interventoría",
        "Investigación":"Investigación",
        "Jurídica":"Jurídica",
        "Logística y Distribución":"Logística y Distribución",
        "Mantenimiento":"Mantenimiento",
        "Materiales: compras e inventario":"Materiales: compras e inventario",
        "Mercadeo":"Mercadeo",
        "Administración: servicios generales":"Administración: servicios generales",
        "Administrativa y Financiera":"Administrativa y Financiera",
        "Agronomía: naturaleza":"Agronomía: naturaleza",
        "Archivo y Documentación":"Archivo y Documentación",
        "Auditoría, Contraloría e interventoría":"Auditoría, Contraloría e interventoría",
        "Calidad (aseguramiento, gestión y afines)":"Calidad (aseguramiento, gestión y afines)",
        "Comercial, Ventas y Telemercadeo":"Comercial, Ventas y Telemercadeo",
        "Comercio Exterior":"Comercio Exterior",
        "Compras e Inventarios":"Compras e Inventarios",
        "Construcción y Obra":"Construcción y Obra",
        "Consultoría":"Consultoría",
        "Consumo masivo":"Consumo masivo",
        "Contabildiad: cartera y costos":"Contabildiad: cartera y costos",
        "Costos y presupuestos":"Costos y presupuestos",
        "Diseño y publicidad":"Diseño y publicidad",
        "Distribución o logística de transporte":"Distribución o logística de transporte",

    }
    aspSal={
        'Menos de $1.000.000':'Menos de $1.000.000',
        '$1.000.000 a $1.500.000':'$1.000.000 a $1.500.000',
        '$1.500.000 a $2.000.000':'$1.500.000 a $2.000.000',
        '$2.000.000 a $2.500.000':'$2.000.000 a $2.500.000',
        '$2.500.000 a $3.000.000':'$2.500.000 a $3.000.000',
        '$3.000.000 a $3.500.000':'$3.000.000 a $3.500.000',
        '$3.500.000 a $4.000.000':'$3.500.000 a $4.000.000',
        '$4.000.000 a $4.500.000':'$4.000.000 a $4.500.000',
        '$4.500.000 a $5.500.000':'$4.500.000 a $5.500.000',
        '$5.500.000 a $6.000.000':'$5.500.000 a $6.000.000',
        '$6.000.000 a $8.000.000':'$6.000.000 a $8.000.000',
        '$8.000.000 a $10.000.000':'$8.000.000 a $10.000.000',
        '$10.000.000 a $12.500.000':'$10.000.000 a $12.500.000',
        '$12.500.000 a $15.000.000':'$12.500.000 a $15.000.000',
        '$15.000.000 a $18.000.000':'$15.000.000 a $18.000.000',
        '$18.000.000 a $21.000.000':'$18.000.000 a $21.000.000',
        'Más de $21.000.000':'Más de $21.000.000',
    }
    trabajoEnCrystal={
        'No aplica':'No aplica',
        'CRYSTAL S.A.S.':'CRYSTAL S.A.S.',
        'INDUSTRIAS PRINTEX S.A.S.':'INDUSTRIAS PRINTEX S.A.S.',
        'NICOLE S.A.S.':'NICOLE S.A.S.',
        'COLHILADOS LTD.':'COLHILADOS LTD.',
        'PLANTAS CIMARRONA LTDA.':'PLANTAS CIMARRONA LTDA.'
    }    

    nivel={
        'Alto':'Alto',
        'Medio':'Medio',
        'Bajo':'Bajo'
    }

    tarProfe={
        'Si':'Si',
        'No':'No',
        'En_Proceso':'En Proceso'
    }

    tarjetaPro=""
    for t in tarProfe:
        tarjetaPro = tarjetaPro + "<option value=\""+t+"\">"+tarProfe[t]+"</option>" +"*"

    mesEstu=""
    for m in meses:
        mesEstu = mesEstu + "<option value=\""+m['mes']+"\">"+m['mes']+"</option>" +"*"

    anioEstu=""
    for a in anios:
        anioEstu = anioEstu + "<option value=\""+str(a)+"\">"+str(a)+"</option>" +"*"

    tipoVia = {
        'AEROPUERTO':'AEROPUERTO',
        'APARTADO':'APARTADO',
        'AUTOPISTA':'AUTOPISTA',
        'AVENIDA':'AVENIDA',
        'CALLE':'CALLE',
        'CARRERA':'CARRERA',
        'CARRETERA':'CARRETERA',
        'CENTRO COMERCIAL':'CENTRO COMERCIAL',
        'CIRCULAR':'CIRCULAR',
        'CORREGIMIENTO':'CORREGIMIENTO',
        'FINCA':'FINCA',
        'GLORIETA':'GLORIETA',
        'KILÓMETRO':'KILÓMETRO',
        'LOTE':'LOTE',
        'MANZANA':'MANZANA',
        'TERMINAL':'TERMINAL',
        'TRANSVERSAL':'TRANSVERSAL',
        'VARIANTE':'VARIANTE',
        'VEREDA':'VEREDA'
    }

    letraDire={
        'A':'A',
        'AA':'AA',
        'AAA':'AAA',
        'AB':'AB',
        'AC':'AC',
        'AF':'AF',
        'B':'B',
        'BB':'BB',
        'BBB':'BBB',
        'BC':'BC',
        'BD':'BD',
        'BE':'BE',
        'C':'C',
        'CC':'CC',
        'CCC':'CCC',
        'D':'D',
        'DA':'DA',
        'DB':'DB',
        'DD':'DD',
        'DDD':'DDD',
        'E':'E',
        'EE':'EE',
        'EEE':'EEE',
        'F':'F',
        'FF':'FF',
        'FFF':'FFF',
        'G':'G',
        'GG':'GG',
        'GGG':'GGG',
        'H':'H',
        'HA':'HA',
        'HB':'HB',
        'HC':'HC',
        'HD':'HD',
        'HE':'HE',
        'HF':'HF',
        'HG':'HG',
        'I':'I',
        'IA':'IA',
        'IB':'IB',
        'IC':'IC',
        'ID':'ID',
        'IE':'IE',
        'IF':'IF',
        'IG':'IG',
        'J':'J',
        'JA':'JA',
        'JB':'JB',
        'JC':'JC',
        'JD':'JD',
        'JE':'JE',
        'JF':'JF',
        'JG':'JG',
        'K':'K',
        'KA':'KA',
        'KB':'KB',
        'KC':'KC',
        'KD':'KD',
        'KE':'KE',
        'KF':'KF',
        'KG':'KG',
        'L':'L',
        'LA':'LA',
        'LB':'LB',
        'LC':'LC',
        'LD':'LD',
        'LE':'LE',
        'LF':'LF',
        'LG':'LG',
        'M':'M',
        'MA':'MA',
        'MB':'MB',
        'MC':'MC',
        'MD':'MD',
        'ME':'ME',
        'MF':'MF',
        'MG':'MG',
        'N':'N',
        'NA':'NA',
        'NB':'NB',
        'NC':'NC',
        'ND':'ND',
        'NE':'NE',
        'NF':'NF',
        'NG':'NG',
        'O':'O',
        'OA':'OA',
        'OB':'OB',
        'OC':'OC',
        'OD':'OD',
        'OE':'OE',
        'OF':'OF',
        'OG':'OG',
        'P':'P',
        'PA':'PA',
        'PB':'PB',
        'PC':'PC',
        'PD':'PD',
        'PE':'PE',
        'PF':'PF',
        'PG':'PG',
        'Q':'Q',
        'QA':'QA',
        'QB':'QB',
        'QC':'QC',
        'QD':'QD',
        'QE':'QE',
        'QF':'QF',
        'QG':'QG',
        'R':'R',
        'RA':'RA',
        'RB':'RB',
        'RC':'RC',
        'RD':'RD',
        'RE':'RE',
        'RF':'RF',
        'RG':'RG',
        'S':'S',
        'SA':'SA',
        'SB':'SB',
        'SC':'SC',
        'SD':'SD',
        'SE':'SE',
        'SF':'SF',
        'SG':'SG',
        'T':'T',
        'TA':'TA',
        'TB':'TB',
        'TC':'TC',
        'TD':'TD',
        'TE':'TE',
        'TF':'TF',
        'TG':'TG',
        'U':'U',
        'UA':'UA',
        'UB':'UB',
        'UC':'UC',
        'UD':'UD',
        'UE':'UE',
        'UF':'UF',
        'UG':'UG',
        'V':'V',
        'VA':'VA',
        'VB':'VB',
        'VC':'VC',
        'VD':'VD',
        'VE':'VE',
        'VF':'VF',
        'VG':'VG',
        'W':'W',
        'WA':'WA',
        'WB':'WB',
        'WC':'WC',
        'WD':'WD',
        'WE':'WE',
        'WF':'WF',
        'WG':'WG',
        'X':'X',
        'XA':'XA',
        'XB':'XB',
        'XC':'XC',
        'XD':'XD',
        'XE':'XE',
        'XF':'XF',
        'XG':'XG',
        'Y':'Y',
        'YA':'YA',
        'YB':'YB',
        'YC':'YC',
        'YD':'YD',
        'YE':'YE',
        'YF':'YF',
        'YG':'YG',
        'Z':'Z',
        'ZA':'ZA',
        'ZB':'ZB',
        'ZC':'ZC',
        'ZD':'ZD',
        'ZE':'ZE',
        'ZF':'ZF',
        'ZG':'ZG',

    }

    cuadrante={
        'Sin selección':'Sin selección',
        'ESTE':'ESTE',
        'NORTE':'NORTE',
        'OESTE':'OESTE',
        'SUR':'SUR'

    }

    claseVivienda={
        'APARTAMENTO':'APARTAMENTO',
        'CASA':'CASA',
        'CASA - LOTE':'CASA - LOTE',
        'CUARTO COMPARTIDO':'CUARTO COMPARTIDO',
        'FINCA':'FINCA',
        'HABITACIÓN':'HABITACIÓN',
        'INQUILINATO':'INQUILINATO',
        'RESIDENCIA':'RESIDENCIA'

    }

    context={'idCargos': idCargos, 'resultPais':resultPais, 'formacion':formac, 'tarProfe':tarjetaPro, 'mesEstu':mesEstu, 'anioEstu':anioEstu,
    'idi':idi,'area':area,'documento':documento,'aspSal':aspSal, 'dias':dias,'meses':meses, 'areaInteres':areaInteres,
    'trabajoEnCrystal': trabajoEnCrystal,'resultDepart':resultDepart,'anios':anios,'nivel':nivel,'tipoVia':tipoVia,
    'letraDire':letraDire,'cuadrante':cuadrante,'claseVivienda':claseVivienda}

    return render(request, 'App/formulario.html', context)

def inicializarLog():
    logger = logging.getLogger("crystal.trabajo")
    logHandler = handlers.TimedRotatingFileHandler("logs/app.log", when='d', interval=1)
    logHandler.setLevel(logging.ERROR)    
    logger.addHandler(logHandler)

    return logger

def enviarForm(request):   
    logger=inicializarLog()
    try: 
        fecha_creacion = datetime.now()
        fecha_creacion.strftime("%Y-%m-%d")
        logger.error("------ Inicia un nuevo registro "+str(fecha_creacion.strftime("%Y-%m-%d %H:%M:%S"))+" ------")
        logger.error("User agent: " +str(request.META['HTTP_USER_AGENT']))
        direccion_equipo = socket.gethostbyname(socket.gethostname())
        logger.error("IP del equipo: "+direccion_equipo)
        #headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
        #response = requests.get("http://localhost:8000/", headers=headers)
        correo=request.POST.get('email','default')
        nombres = request.POST.get('nombres','default')
        apellidos = request.POST.get('apellidos','default')
        logger.error("nombre: "+nombres + " " +apellidos)
        idCargos = request.POST.get('cargo','default')
        cargos=int(idCargos)
        print(str(cargos)+" cargos")
        cargo=Cargo.objects.get(id=cargos)
        logger.error("Cargo: " + str(cargo))
        formacion1 = str(request.POST.get('formacion1','default')).replace("_"," ")
        formacion2 = str(request.POST.get('formacion2','default')).replace("_"," ")
        formacion3 = str(request.POST.get('formacion3','default')).replace("_"," ")
        formacion4 = str(request.POST.get('formacion4','default')).replace("_"," ")
        tarProfe1 = str(request.POST.get('tarProfe1','default')).replace("_"," ")
        tarProfe2 = str(request.POST.get('tarProfe2','default')).replace("_"," ")
        tarProfe3 = str(request.POST.get('tarProfe3','default')).replace("_"," ")
        tarProfe4 = str(request.POST.get('tarProfe4','default')).replace("_"," ")
        direccion = request.POST.get('address','default')
        
        print("dire " +direccion)
        ar=request.FILES.get('archivoHV', None)
        archivo= "/media/App/"+ str(ar)
        mime=mimetypes.guess_type(archivo, strict=True)[0]
        if mime == "application/pdf" or mime == "application/msword":
            archivoHV=ar
        else:
            archivoHV=None   
            
        logger.error("Archivo: " + str(archivo))

        Personas_Postulada.objects.create(
            cargo=cargo,
            correo=correo,
            telefono=request.POST.get('telefono','default'),
            telefono_adicional=request.POST.get('telefonoOp','default'),
            identificacion=request.POST.get('documento','default'),
            numero_identificacion=request.POST.get('identificacion','default'),
            nombres=nombres,
            apellidos=apellidos,
            fecha_nacimiento=request.POST.get('fechaNac','default'),
            pais_nacimiento=request.POST.get('paisNacim','default'),
            departamento_nacimiento=request.POST.get('depNac','default'),
            ciudad_nacimiento=request.POST.get('ciudadNac','default'),
            genero=request.POST.get('genero','default'),
            soy_empleado = request.POST.get('trabajoEnCrystal','default'),
            direccion=direccion,
            departamento_residencia=request.POST.get('depResi','default'),
            municipio_residencia=request.POST.get('ciudadResi','default'),
            formacion_1=formacion1,
            formacion_2=formacion2,
            formacion_3=formacion3,
            formacion_4=formacion4,  
            area_formacion_1=request.POST.get('areasEst1','default'),
            area_formacion_2=request.POST.get('areasEst2','default'),
            area_formacion_3=request.POST.get('areasEst3','default'),
            area_formacion_4=request.POST.get('areasEst4','default'),
            institucion_1=request.POST.get('institucion1','default'),
            institucion_2=request.POST.get('institucion2','default'),
            institucion_3=request.POST.get('institucion3','default'),
            institucion_4=request.POST.get('institucion4','default'),
            tarjeta_profesional_1=tarProfe1,
            tarjeta_profesional_2=tarProfe2,
            tarjeta_profesional_3=tarProfe3,
            tarjeta_profesional_4=tarProfe4,
            fecha_finalizacion_estudio_1=request.POST.get('fechaEstu1','default'),
            fecha_finalizacion_estudio_2=request.POST.get('fechaEstu2','default'),
            fecha_finalizacion_estudio_3=request.POST.get('fechaEstu3','default'),
            fecha_finalizacion_estudio_4=request.POST.get('fechaEstu4','default'),
            fecha_finalizacion_experiencia_1=request.POST.get('fechaExp1','default'),
            fecha_finalizacion_experiencia_2=request.POST.get('fechaExp2','default'),
            fecha_finalizacion_experiencia_3=request.POST.get('fechaExp3','default'),
            fecha_finalizacion_experiencia_4=request.POST.get('fechaExp4','default'),
            fecha_finalizacion_experiencia_5=request.POST.get('fechaExp5','default'),
            fecha_finalizacion_experiencia_6=request.POST.get('fechaExp6','default'),
            fecha_finalizacion_experiencia_7=request.POST.get('fechaExp7','default'),
            fecha_finalizacion_experiencia_8=request.POST.get('fechaExp8','default'),
            fecha_finalizacion_experiencia_9=request.POST.get('fechaExp9','default'),
            fecha_finalizacion_experiencia_10=request.POST.get('fechaExp10','default'),
            idioma_1=request.POST.get('idioma1','default'),
            nivel_idioma_1=request.POST.get('nivel1','default'),
            idioma_2=request.POST.get('idioma2','default'),
            nivel_idioma_2=request.POST.get('nivel2','default'),
            idioma_3=request.POST.get('idioma3','default'),
            nivel_idioma_3=request.POST.get('nivel3','default'),
            empresa_1=request.POST.get('empresa1','default'),
            cargo_1=request.POST.get('cargo1','default'),
            funciones_y_logros_1=request.POST.get('funciones1','default'),
            empresa_2=request.POST.get('empresa2','default'),
            cargo_2=request.POST.get('cargo2','default'),
            funciones_y_logros_2=request.POST.get('funciones2','default'),
            empresa_3=request.POST.get('empresa3','default'),
            cargo_3=request.POST.get('cargo3','default'),
            funciones_y_logros_3=request.POST.get('funciones3','default'),
            empresa_4=request.POST.get('empresa4','default'),
            cargo_4=request.POST.get('cargo4','default'),
            funciones_y_logros_4=request.POST.get('funciones4','default'),
            empresa_5=request.POST.get('empresa5','default'),
            cargo_5=request.POST.get('cargo5','default'),
            funciones_y_logros_5=request.POST.get('funciones5','default'),
            empresa_6=request.POST.get('empresa6','default'),
            cargo_6=request.POST.get('cargo6','default'),
            funciones_y_logros_6=request.POST.get('funciones6','default'),
            empresa_7=request.POST.get('empresa7','default'),
            cargo_7=request.POST.get('cargo7','default'),
            funciones_y_logros_7=request.POST.get('funciones7','default'),
            empresa_8=request.POST.get('empresa8','default'),
            cargo_8=request.POST.get('cargo8','default'),
            funciones_y_logros_8=request.POST.get('funciones8','default'),
            empresa_9=request.POST.get('empresa9','default'),
            cargo_9=request.POST.get('cargo9','default'),
            funciones_y_logros_9=request.POST.get('funciones9','default'),
            empresa_10=request.POST.get('empresa10','default'),
            cargo_10=request.POST.get('cargo10','default'),
            funciones_y_logros_10=request.POST.get('funciones10','default'),
            areas_de_interes=request.POST.get('areasInte','default'),
            otras_areas_de_interes=request.POST.get('areaInteOtr','default'),
            ultimo_salario=request.POST.get('ultiSal','default'),
            aspiracion_salarial=request.POST.get('aspSal','default'),
            archivo_HV=archivoHV,
            referido_por="N/A",
            comentarios="N/A",
            fecha_creacion=fecha_creacion
        )
        logger.error("se guardó en la BD")
        #time.sleep(10)
        if cargos==1:
            nombreImagen="AUTORESPUESTASIN"
        else:
            nombreImagen="AUTORESPUESTA"
        
        subject="Hemos recibido tu hoja de vida"
        mensaje='<html><h1>Hola '+nombres+',</h1><body><img src=cid:'+nombreImagen+'></body></html>'
        msg = EmailMessage(subject,mensaje,settings.DEFAULT_FROM_EMAIL,[correo])
        rutaImagen="App/static/App/images/"+nombreImagen+".jpg"
        file = open(rutaImagen, "rb").read()
        attach_image = MIMEImage(file, 'jpg')
        attach_image.add_header('Content-ID', '<'+nombreImagen+'>')
        attach_image.add_header('Content-Disposition', 'attachment', filename=nombreImagen)
        msg.attach(attach_image)
        msg.content_subtype="html"
        msg.send()
        logger.error("se envío el correo")
        
    except Exception as e:
        logger.error(str(e))
        return JsonResponse(status=500, data="Error haciendo el registro", safe=False)

    logger.handlers[0].flush()
    return JsonResponse('Registro completo!', safe=False)