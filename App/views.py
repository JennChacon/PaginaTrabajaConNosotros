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
        "Administraci??n":"Administraci??n",
        "Agronom??a":"Agronom??a",
        "Antropolog??a, Artes Liberales":"Antropolog??a, Artes Liberales",
        "Arquitectura y afines":"Arquitectura y afines",
        "Artes Pl??sticas, Visuales y afines":"Artes Pl??sticas, Visuales y afines",
        "Artes Representativas":"Artes Representativas",
        "Bacteriolog??a":"Bacteriolog??a",
        "Bibliotecolog??a, otros de Ciencias Sociales y Humanas":"Bibliotecolog??a, otros de Ciencias Sociales y Humanas",
        "Biolog??a, Microbiolog??a y afines":"Biolog??a, Microbiolog??a y afines",
        "Ciencia Pol??tica, Relaciones Internacionales":"Ciencia Pol??tica, Relaciones Internacionales",
        "Comunicaci??n Social, Periodismo y afines":"Comunicaci??n Social, Periodismo y afines",
        "Contadur??a P??blica":"Contadur??a P??blica",
        "Deportes, Educaci??n F??sica y Recreaci??n":"Deportes, Educaci??n F??sica y Recreaci??n",
        "Derecho y afines":"Derecho y afines",
        "Dise??o":"Dise??o",
        "Econom??a":"Econom??a",
        "Educaci??n":"Educaci??n",
        "Enfermer??a":"Enfermer??a",
        "Filosof??a, Teolog??a y afines":"Filosof??a, Teolog??a y afines",
        "F??sica":"F??sica",
        "Formaci??n relacionada con el campo militar o policial":"Formaci??n relacionada con el campo militar o policial",
        "Geograf??a, Historia":"Geograf??a, Historia",
        "Geolog??a, otros programas de Ciencias Naturales":"Geolog??a, otros programas de Ciencias Naturales",
        "Ingenier??a Administrativa y afines":"Ingenier??a Administrativa y afines",
        "Ingenier??a Agr??cola, Forestal y afines":"Ingenier??a Agr??cola, Forestal y afines",
        "Ingenier??a Agroindustrial, Alimentos y afines":"Ingenier??a Agroindustrial, Alimentos y afines",
        "Ingenier??a Agr??noma, Pecuaria y afines":"Ingenier??a Agr??noma, Pecuaria y afines",
        "Ingenier??a Ambiental, Sanitaria y afines":"Ingenier??a Ambiental, Sanitaria y afines",
        "Ingenier??a Biom??dica y afines":"Ingenier??a Biom??dica y afines",
        "Ingenier??a Civil y afines":"Ingenier??a Civil y afines",
        "Ingenier??a de Minas, Metalurgia y afines":"Ingenier??a de Minas, Metalurgia y afines",
        "Ingenier??a de Sistemas, Telem??tica y afines":"Ingenier??a de Sistemas, Telem??tica y afines",
        "Ingenier??a El??ctrica y afines":"Ingenier??a El??ctrica y afines",
        "Ingenier??a Electr??nica, Telecomunicaciones y afines":"Ingenier??a Electr??nica, Telecomunicaciones y afines",
        "Ingenier??a Industrial y afines":"Ingenier??a Industrial y afines",
        "Ingenier??a Mec??nica y afines":"Ingenier??a Mec??nica y afines",
        "Ingenier??a Qu??mica y afines":"Ingenier??a Qu??mica y afines",
        "Instrumentaci??n Quir??rgica":"Instrumentaci??n Quir??rgica",
        "Lenguas Modernas, Literatura, Ling????stica y afines":"Lenguas Modernas, Literatura, Ling????stica y afines",
        "Matem??ticas, Estad??stica y afines":"Matem??ticas, Estad??stica y afines",
        "Medicina":"Medicina",
        "Medicina Veterinaria":"Medicina Veterinaria",
        "M??sica":"M??sica",
        "Nutrici??n y Diet??tica":"Nutrici??n y Diet??tica",
        "Odontolog??a":"Odontolog??a",
        "Optometr??a, otros programas de Ciencias de la Salud":"Optometr??a, otros programas de Ciencias de la Salud",
        "Otras Ingenier??as":"Otras Ingenier??as",
        "Otros programas asociados a Bellas Artes":"Otros programas asociados a Bellas Artes",
        "Psicolog??a":"Psicolog??a",
        "Publicidad y afines":"Publicidad y afines",
        "Qu??mica y afinas":"Qu??mica y afinas",
        "Salud P??blica":"Salud P??blica",
        "Sociolog??a, Trabajo Social y afines":"Sociolog??a, Trabajo Social y afines",
        "Terapias":"Terapias",
        "Zootecnia":"Zootecnia",
    }
    areaEst=[]
    if formacion=="Preescolar":
        areaEst.append("Preescolar")
    else:
        if formacion=="B??sica_Primaria_(1_-_5)":
            areaEst.append("B??sica Primaria (1?? - 5??)")
        else:
            if formacion=="B??sica_Secundaria_(6_-_9)":
                areaEst.append("B??sica Secundaria (6?? - 9??)")
            else:
                if formacion=="Media_(10_-_13)":
                    areaEst.append("Bachillerato Acad??mico")
                    areaEst.append("Bachillerato Comercial")
                    areaEst.append("Bachillerato T??cnico")
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
        'C??dula': 'C??dula',  
        'C??dula extranjera':'C??dula extranjera',        
        'Registro civil':'Registro civil',
        'Permiso especial de permanencia':'Permiso especial de permanencia'
    }
    formacion={
        'Preescolar':'Preescolar',
        'B??sica_Primaria_(1_-_5)':'B??sica Primaria (1?? - 5??)',
        'B??sica_Secundaria_(6_-_9)':'B??sica Secundaria (6?? - 9??)',
        'Media_(10_-_13)':'Media (10?? - 13??)',
        'T??cnico_Laboral':'T??cnico Laboral',
        'Formaci??n_Tec_profesional':'Formaci??n Tec profesional',
        'Tecnol??gica':'Tecnol??gica',
        'Universitaria':"Universitaria",
        'Especializaci??n':'Especializaci??n',
        'Maestr??a':'Maestr??a',
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
        'Alban??s':'Alban??s',
        'Alem??n':'Alem??n',
        'Am??rico':'Am??rico',
        '??rabe':'??rabe',
        'Aragon??s':'Aragon??s',
        'Armenio':'Armenio',
        'Asam??s':'Asam??s',
        'Avar':'Avar',
        'Av??stico':'Av??stico',
        'Azer??':'Azer??',
        'Bambara':'Bambara',
        'Baskir':'Baskir',
        'Bengal??':'Bengal??',
        'Bhojpur??':'Bhojpur??',
        'Bielorruso':'Bielorruso',
        'Birmano':'Birmano',
        'Bislama':'Bislama',
        'Bosnio':'Bosnio',
        'Bret??n':'Bret??n',
        'B??lgaro':'B??lgaro',
        'Cachemiro':'Cachemiro',
        'Camboyano':'Camboyano',
        'Canar??s':'Canar??s',
        'Catal??n':'Catal??n',
        'Chamorro':'Chamorro',
        'Checheno':'Checheno',
        'Checo':'Checo',
        'Chichewa':'Chichewa',
        'Chino':'Chino',
        'Chuan':'Chuan',
        'Chuvasio':'Chuvasio',
        'Cingal??s':'Cingal??s',
        'Coreano':'Coreano',
        'C??rnico':'C??rnico',
        'Corso':'Corso',
        'Cree':'Cree',
        'Croata':'Croata',
        'Dan??s':'Dan??s',
        'Dzongkha':'Dzongkha',
        'Eslavo eclesi??stico antiguo':'Eslavo eclesi??stico antiguo',
        'Eslovaco':'Eslovaco',
        'Esloveno':'Esloveno',
        'Espa??ol':'Espa??ol',
        'Esperanto':'Esperanto',
        'Estonio':'Estonio',
        'Ewe':'Ewe',
        'Fero??s':'Fero??s',
        'Fijiano':'Fijiano',
        'Fin??s':'Fin??s',
        'Franc??s':'Franc??s',
        'Fris??n':'Fris??n',
        'Fula':'Fula',
        'Ga??lico escoc??s':'Ga??lico escoc??s',
        'Gal??s':'Gal??s',
        'Gallego':'Gallego',
        'Georgiano':'Georgiano',
        'Griego':'Griego',
        'Groenland??s':'Groenland??s',
        'Guaran??':'Guaran??',
        'Guyarat??':'Guyarat??',
        'Haitiano':'Haitiano',
        'Hausa':'Hausa',
        'Hebreo':'Hebreo',
        'Herero':'Herero',
        'Hindi':'Hindi',
        'Hiri motu':'Hiri motu',
        'H??ngaro':'H??ngaro',
        'Ido':'Ido',
        'Igbo':'Igbo',
        'Indonesio':'Indonesio',
        'Ingl??s':'Ingl??s',
        'Interlingua':'Interlingua',
        'Inuktitut':'Inuktitut',
        'Inupiaq':'Inupiaq',
        'Irland??s':'Irland??s',
        'Island??s':'Island??s',
        'Italiano':'Italiano',
        'Japon??s':'Japon??s',
        'Javan??s':'Javan??s',
        'Kanuri':'Kanuri',
        'Kazajo':'Kazajo',
        'Kikuyu':'Kikuyu',
        'Kirgu??s':'Kirgu??s',
        'Kirundi':'Kirundi',
        'Komi':'Komi',
        'Kongo':'Kongo',
        'Kuanyama':'Kuanyama',
        'Kurdo':'Kurdo',
        'Lao':'Lao',
        'Lat??n':'Lat??n',
        'Let??n':'Let??n',
        'Limburgu??s':'Limburgu??s',
        'Lingala':'Lingala',
        'Lituano':'Lituano',
        'Luba-katanga':'Luba-katanga',
        'Luganda':'Luganda',
        'Luxemburgu??s':'Luxemburgu??s',
        'Macedonio':'Macedonio',
        'Malayalam':'Malayalam',
        'Malayo':'Malayo',
        'Maldivo':'Maldivo',
        'Malgache':'Malgache',
        'Malt??s':'Malt??s',
        'Man??s':'Man??s',
        'Maor??':'Maor??',
        'Marat??':'Marat??',
        'Marshal??s':'Marshal??s',
        'Moldavo':'Moldavo',
        'Mongol':'Mongol',
        'Nauruano':'Nauruano',
        'Navajo':'Navajo',
        'Ndebele del norte':'Ndebele del norte',
        'Ndebele del sur':'Ndebele del sur',
        'Ndonga':'Ndonga',
        'Neerland??s':'Neerland??s',
        'Nepal??':'Nepal??',
        'Noruego':'Noruego',
        'Noruego bokm??l':'Noruego bokm??l',
        'Nynorsk':'Nynorsk',
        'Occidental':'Occidental',
        'Occitano':'Occitano',
        'Ojibwa':'Ojibwa',
        'Oriya':'Oriya',
        'Oromo':'Oromo',
        'Os??tico':'Os??tico',
        'Pali':'Pali',
        'Panyab??':'Panyab??',
        'Past??':'Past??',
        'Persa':'Persa',
        'Polaco':'Polaco',
        'Portugu??s':'Portugu??s',
        'Quechua':'Quechua',
        'Retorrom??nico':'Retorrom??nico',
        'Ruand??s':'Ruand??s',
        'Rumano':'Rumano',
        'Ruso':'Ruso',
        'Sami septentrional':'Sami septentrional',
        'Samoano':'Samoano',
        'Sango':'Sango',
        'S??nscrito':'S??nscrito',
        'Sardo':'Sardo',
        'Serbio':'Serbio',
        'Sesotho':'Sesotho',
        'Setsuana':'Setsuana',
        'Shona':'Shona',
        'Sindhi':'Sindhi',
        'Somal??':'Somal??',
        'Suajili':'Suajili',
        'Suazi':'Suazi',
        'Sueco':'Sueco',
        'Sundan??s':'Sundan??s',
        'Tagalo':'Tagalo',
        'Tahitiano':'Tahitiano',
        'Tailand??s':'Tailand??s',
        'Tamil':'Tamil',
        'T??rtaro':'T??rtaro',
        'Tayiko':'Tayiko',
        'Telug??':'Telug??',
        'Tibetano':'Tibetano',
        'Tigri??a':'Tigri??a',
        'Tongano':'Tongano',
        'Tsonga':'Tsonga',
        'Turco':'Turco',
        'Turcomano':'Turcomano',
        'Twi':'Twi',
        'Ucraniano':'Ucraniano',
        'Uigur':'Uigur',
        'Urdu':'Urdu',
        'Uzbeko':'Uzbeko',
        'Val??n':'Val??n',
        'Vascuence':'Vascuence',
        'Venda':'Venda',
        'Vietnamita':'Vietnamita',
        'Volap??k':'Volap??k',
        'Wolof':'Wolof',
        'Xhosa':'Xhosa',
        'Yi de Sichu??n':'Yi de Sichu??n',
        'Y??dish':'Y??dish',
        'Yoruba':'Yoruba',
        'Zul??':'Zul??',

    }

    idi=""
    for i in idiomas:
        idi = idi + "<option value=\""+i+"\">"+i+"</option>" +"*"

    formac=""
    for i in formacion:
        formac = formac + "<option value=\""+i+"\">"+formacion[i]+"</option>" +"*"

    area={
        "Administraci??n":"Administraci??n",
        "Agronom??a":"Agronom??a",
        "Antropolog??a, Artes Liberales":"Antropolog??a, Artes Liberales",
        "Arquitectura y afines":"Arquitectura y afines",
        "Artes Pl??sticas, Visuales y afines":"Artes Pl??sticas, Visuales y afines",
        "Artes Representativas":"Artes Representativas",
        "Bacteriolog??a":"Bacteriolog??a",
        "Bibliotecolog??a, otros de Ciencias Sociales y Humanas":"Bibliotecolog??a, otros de Ciencias Sociales y Humanas",
        "Biolog??a, Microbiolog??a y afines":"Biolog??a, Microbiolog??a y afines",
        "Ciencia Pol??tica, Relaciones Internacionales":"Ciencia Pol??tica, Relaciones Internacionales",
        "Comunicaci??n Social, Periodismo y afines":"Comunicaci??n Social, Periodismo y afines",
        "Contadur??a P??blica":"Contadur??a P??blica",
        "Deportes, Educaci??n F??sica y Recreaci??n":"Deportes, Educaci??n F??sica y Recreaci??n",
        "Derecho y afines":"Derecho y afines",
        "Dise??o":"Dise??o",
        "Econom??a":"Econom??a",
        "Educaci??n":"Educaci??n",
        "Enfermer??a":"Enfermer??a",
        "Filosof??a, Teolog??a y afines":"Filosof??a, Teolog??a y afines",
        "F??sica":"F??sica",
        "Formaci??n relacionada con el campo militar o policial":"Formaci??n relacionada con el campo militar o policial",
        "Geograf??a, Historia":"Geograf??a, Historia",
        "Geolog??a, otros programas de Ciencias Naturales":"Geolog??a, otros programas de Ciencias Naturales",
        "Ingenier??a Administrativa y afines":"Ingenier??a Administrativa y afines",
        "Ingenier??a Agr??cola, Forestal y afines":"Ingenier??a Agr??cola, Forestal y afines",
        "Ingenier??a Agroindustrial, Alimentos y afines":"Ingenier??a Agroindustrial, Alimentos y afines",
        "Ingenier??a Agr??noma, Pecuaria y afines":"Ingenier??a Agr??noma, Pecuaria y afines",
        "Ingenier??a Ambiental, Sanitaria y afines":"Ingenier??a Ambiental, Sanitaria y afines",
        "Ingenier??a Biom??dica y afines":"Ingenier??a Biom??dica y afines",
        "Ingenier??a Civil y afines":"Ingenier??a Civil y afines",
        "Ingenier??a de Minas, Metalurgia y afines":"Ingenier??a de Minas, Metalurgia y afines",
        "Ingenier??a de Sistemas, Telem??tica y afines":"Ingenier??a de Sistemas, Telem??tica y afines",
        "Ingenier??a El??ctrica y afines":"Ingenier??a El??ctrica y afines",
        "Ingenier??a Electr??nica, Telecomunicaciones y afines":"Ingenier??a Electr??nica, Telecomunicaciones y afines",
        "Ingenier??a Industrial y afines":"Ingenier??a Industrial y afines",
        "Ingenier??a Mec??nica y afines":"Ingenier??a Mec??nica y afines",
        "Ingenier??a Qu??mica y afines":"Ingenier??a Qu??mica y afines",
        "Instrumentaci??n Quir??rgica":"Instrumentaci??n Quir??rgica",
        "Lenguas Modernas, Literatura, Ling????stica y afines":"Lenguas Modernas, Literatura, Ling????stica y afines",
        "Matem??ticas, Estad??stica y afines":"Matem??ticas, Estad??stica y afines",
        "Medicina":"Medicina",
        "Medicina Veterinaria":"Medicina Veterinaria",
        "M??sica":"M??sica",
        "Nutrici??n y Diet??tica":"Nutrici??n y Diet??tica",
        "Odontolog??a":"Odontolog??a",
        "Optometr??a, otros programas de Ciencias de la Salud":"Optometr??a, otros programas de Ciencias de la Salud",
        "Otras Ingenier??as":"Otras Ingenier??as",
        "Otros programas asociados a Bellas Artes":"Otros programas asociados a Bellas Artes",
        "Psicolog??a":"Psicolog??a",
        "Publicidad y afines":"Publicidad y afines",
        "Qu??mica y afinas":"Qu??mica y afinas",
        "Salud P??blica":"Salud P??blica",
        "Sociolog??a, Trabajo Social y afines":"Sociolog??a, Trabajo Social y afines",
        "Terapias":"Terapias",
        "Zootecnia":"Zootecnia",
    }
    areaInteres={
        "Mercadeo y publicidad":"Mercadeo y publicidad",
        "Obra":"Obra",
        "Operaciones y procesos":"Operaciones y procesos",
        "Organizaci??n y m??todos":"Organizaci??n y m??todos",
        "Producci??n":"Producci??n",
        "Proyectos (an??lisis, desarrollo, gesti??n y afines)":"Proyectos (an??lisis, desarrollo, gesti??n y afines)",
        "Recepci??n":"Recepci??n",
        "Recursos Humanos y Admon. de Personal":"Recursos Humanos y Admon. de Personal",
        "Redacci??n y Generaci??n de Contenido":"Redacci??n y Generaci??n de Contenido",
        "Salud":"Salud",
        "Secretariado":"Secretariado",
        "Seguridad Industrial, Ambiental y Ocupacional":"Seguridad Industrial, Ambiental y Ocupacional",
        "Servicio al Cliente":"Servicio al Cliente",
        "Servicios Generales, Aseo y Vigilancia":"Servicios Generales, Aseo y Vigilancia",
        "Sistemas":"Sistemas",
        "Sistemas y tecnolog??a":"Sistemas y tecnolog??a",
        "Telemercadeo":"Telemercadeo",
        "Ventas":"Ventas",
        "Facturaci??n":"Facturaci??n",
        "Financiera: cr??dito y tesorer??a":"Financiera: cr??dito y tesorer??a",
        "Gerencia General (cargos corporativos)":"Gerencia General (cargos corporativos)",
        "Instalaci??n y Reparaciones t??cnicas":"Instalaci??n y Reparaciones t??cnicas",
        "Interventor??a":"Interventor??a",
        "Investigaci??n":"Investigaci??n",
        "Jur??dica":"Jur??dica",
        "Log??stica y Distribuci??n":"Log??stica y Distribuci??n",
        "Mantenimiento":"Mantenimiento",
        "Materiales: compras e inventario":"Materiales: compras e inventario",
        "Mercadeo":"Mercadeo",
        "Administraci??n: servicios generales":"Administraci??n: servicios generales",
        "Administrativa y Financiera":"Administrativa y Financiera",
        "Agronom??a: naturaleza":"Agronom??a: naturaleza",
        "Archivo y Documentaci??n":"Archivo y Documentaci??n",
        "Auditor??a, Contralor??a e interventor??a":"Auditor??a, Contralor??a e interventor??a",
        "Calidad (aseguramiento, gesti??n y afines)":"Calidad (aseguramiento, gesti??n y afines)",
        "Comercial, Ventas y Telemercadeo":"Comercial, Ventas y Telemercadeo",
        "Comercio Exterior":"Comercio Exterior",
        "Compras e Inventarios":"Compras e Inventarios",
        "Construcci??n y Obra":"Construcci??n y Obra",
        "Consultor??a":"Consultor??a",
        "Consumo masivo":"Consumo masivo",
        "Contabildiad: cartera y costos":"Contabildiad: cartera y costos",
        "Costos y presupuestos":"Costos y presupuestos",
        "Dise??o y publicidad":"Dise??o y publicidad",
        "Distribuci??n o log??stica de transporte":"Distribuci??n o log??stica de transporte",

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
        'M??s de $21.000.000':'M??s de $21.000.000',
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
        'KIL??METRO':'KIL??METRO',
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
        'Sin selecci??n':'Sin selecci??n',
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
        'HABITACI??N':'HABITACI??N',
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
        logger.error("se guard?? en la BD")
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
        logger.error("se env??o el correo")
        
    except Exception as e:
        logger.error(str(e))
        return JsonResponse(status=500, data="Error haciendo el registro", safe=False)

    logger.handlers[0].flush()
    return JsonResponse('Registro completo!', safe=False)