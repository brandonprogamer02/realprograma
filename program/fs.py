import sqlite3
import requests
from os import path
import os
import sys
import json
from datetime import date, timedelta
from playsound import playsound
signo_zodiaco = ''
diccionariossignos = {}
reallista = []

def get_data_cedula2(cedula1):
    url = 'http://173.249.49.169:88/api/test/consulta/'
    
    h = str(cedula1)
    j = str(h).zfill(11)
    
    try:
        response = requests.get(url + j)
    except ConnectionError:
        print('no hay conexion a internet')
    try:
        parseo_json = json.loads(response.content.decode('utf-8'))
    except ValueError:
        print 'la cedula que has introducido es incorrecta'
        raw_input()
        menu()
    
    
   
    fecha_nacimiento = str(parseo_json['FechaNacimiento'])
    nombre = str(parseo_json['Nombres'])
    apellidos = str(parseo_json['Apellido1'] + " " +  parseo_json['Apellido2'])
    aa_zodiaco = int(fecha_nacimiento[0:4])
    mm_zodiaco = int(fecha_nacimiento[5:7])
    dd_zodiaco = int(fecha_nacimiento[8:10])
    foto = str(parseo_json['Foto'])
    
    
    evaluar(mm_zodiaco,dd_zodiaco)
    return nombre,apellidos,aa_zodiaco,mm_zodiaco,dd_zodiaco,foto

def agregar():
    global reallista
    os.system('cls')
    os.system('color 5f')
    print('\n     Agregar people:\n')
    try:
        playsound('Introducecedula.wav')
        cedula = str(raw_input('Porfavor ingresa la cedula: '))
    except ValueError:
        print('Debes ingresar un valor numerico')
        playsound('Introducecedula.wav')
        cedula = str(raw_input('Porfavor ingresa la cedula: '))

    playsound('Ingresasexo.wav')
    sexo = str(raw_input('Porfavor ingresa el sexo: '))
    nacionalidad = 'Nacionalidad Dominicana'
    playsound('Estado paciente.wav')
    estado = str(raw_input('Porfavor ingresa el estado del paciente: '))
    try:
        playsound('Ingresa Telefoni.wav')
        telefono = raw_input('Porfavor ingresa el telefono: ')
    except ValueError:
        print('Debes ingresar un valor numerico')
        playsound('Ingresa Telefoni.wav')
        telefono = int(raw_input('Porfavor ingresa el telefono: '))

    playsound('Ingresacorreo.wav')
    correo = str(raw_input('Porfavor ingresa el correo: '))
    playsound('Ingresa latitud.wav')
    latitud = str(raw_input('Porfavor ingresa la latitud: '))
    playsound('Ingresa longitud.wav')
    longitud = str(raw_input('Porfavor ingresa la longitud: '))
    playsound('Ingresa provincia.wav')
    provincia = str(raw_input('Porfavor ingresa la provincia: '))
    
    
    datosapi = get_data_cedula2(cedula)
    
    h = str(cedula)
    j = str(h).zfill(11)
    

    nombre = str(datosapi[0])
    
    apellido = str(datosapi[1])
    fecha_nac = str(datosapi[2]) + '/' + str(datosapi[3]) + '/' + str(datosapi[4])

    # se crea una tupla donde se guardaran todos los datos; esta tupla se metera dentro de una lista
    
    realtupla = (j,nombre,apellido,sexo,fecha_nac,nacionalidad,estado,telefono,correo,latitud,longitud,provincia)
    
    reallista.append(realtupla)
    
    
    # creacion de la conexion
    conexion = sqlite3.connect('database')
    # creacion del cursor
    cursor = conexion.cursor()
    # verificacion de si existe el archivo para proceder a creat la tabla correspodiente
    
        
    # se insertan los datos
    try:
        cursor.executemany('INSERT INTO personas VALUES(?,?,?,?,?,?,?,?,?,?,?,?)' ,reallista)
    except sqlite3.IntegrityError:
        playsound('aa.wav')
        print 'no se puede ingresar dos veces el mismo paciente'
        raw_input('presiona tecla para continuar')
        menu()

    j = "'"+j+"'"
    reallista = []
    texto = 'select * from personas where cedula = ' + j
    
    
    cursor.execute(texto)
    data = cursor.fetchall()
    conexion.commit()
    conexion.close()
    
    raw_input('presiona una tecla para continuar')
    # mandar mensaje telegram
    for data in data:
        realmensaje = '     \n     cedula: '+str(data[0])+'\n''     nombre: '+str(data[1])+' \n     Apellido: '+str(data[2])+' \n     sexo: '+str(data[3])+' \n     fecha_nacimiento '+str(data[4])+' \n     nacionalidad: '+str(data[5])+' \n     estado: '+str(data[6])+' \n     Telefono: '+str(data[7])+'\n'+'     Correo: '+str(data[8])+' \n     Latitud: '+str(data[9])+' \n     Longitud: '+str(data[10])+' \n     Provincia: '+str(data[11])
        print 'este es el real mensaje: ' + realmensaje

    userid = open('userid.txt').read()
    try:
        sendMessage('se registrado un nuevo caso:\n',userid)
        sendMessage(realmensaje,userid)

        print 'se ha enviado el mensaje correctamente al canal de telegram'
        
    except NameError:
        print 'no se ha enviado el mensaje al canal de telegram porque no te has registrado'

    # se cierran conexiones
    print '\n\nQuieres seguir intentando?\n'
    print '(Si o No)'
    answer = raw_input('ingresa tu respuesta: ')
    if answer == 'si':
        agregar()
    elif answer == 'no':
        menu()
    else:
        menu()

def listado():
    os.system('cls')
    os.system('color 4f')
    conexion = sqlite3.connect('database')
    cursor = conexion.cursor()
    playsound('Eligido mostrar casos.wav')
    # se lanza la instruccion de sql SELECT con la cual se puede extraer todos los datos de personas
    cursor.execute('SELECT * FROM personas')
    # con .fetchall() se almacenan los datos recopilados
    data = cursor.fetchall()
    # con un bucle for recorremos ese objeto donde se a almacenado los datos con el .fetchall()
    # para poder extraer de forma limpia y ordenada esos datos
    print '\n Este es el listado de Casos \n'
    for data in data:
        print'     \n     cedula: ',str(data[0]),'\n''     nombre: ',str(data[1]),' \n     Apellido: ',str(data[2]),' \n     sexo: ',str(data[3]),' \n     fecha_nacimiento ',str(data[4]),' \n     nacionalidad: ',str(data[5]),' \n     estado: ',str(data[6]),' \n     Telefono: ',str(data[7]),'\n','     Correo: ',str(data[8]),' \n     Latitud: ',str(data[9]),' \n     Longitud: ',str(data[10]),' \n     Provincia: ',str(data[11])
        print'======================================================================================================================================='

    # se cierran connections
    conexion.commit()
    conexion.close()
    raw_input('Vas a volver al Menu...')
    playsound('Volver al menu.wav')
    menu()

def editar():
    os.system('color 2f')
    global reallista
    playsound('Elegido editar casos.wav')
    # variable para verificar si encuentra alguna coincidencia en la busqueda del registro
    comprobacionn = False
    playsound('Introducecedula/wav')
    re = raw_input('Porfavor ingresa la cedula de la persona para poder editarla:')
    conexion = sqlite3.connect('database')
    cursor = conexion.cursor()

    cursor.execute('SELECT * FROM personas')
    realesdatos = cursor.fetchall()


    for asd in realesdatos:
        iii = str(asd[0])
        comprobacion = iii.find(re)
        if comprobacion != -1:
            playsound('')
            nombre = raw_input('\nPorfavor ingresa el nombre: ')
            apellido = raw_input('\nPorfavor ingresa el apellido: ')
            sexo = raw_input('\nPorfavor ingresa el sexo: ')
            fecha_nac = raw_input('\nPorfavor ingresa la fecha de nacimiento: ')
            nacionalidad = raw_input('\nPorfavor ingresa la nacionalidad: ')
            estado = raw_input('\nPorfavor ingresa el estado del paciente: ')
            telefono = raw_input('\nPorfavor ingresa el telefono: ')
            correo = raw_input('\nPorfavor ingresa el correo: ')
            latitud = raw_input('\nPorfavor ingresa la latitud: ')
            longitud = raw_input('\nPorfavor ingresa la longitud: ')
            provincia = raw_input('\nPorfavor ingresa la provincia: ')
            re = "'"+re+"'"
            realtupla1 = (nombre,apellido,sexo,fecha_nac,nacionalidad,estado,telefono,correo,latitud,longitud,provincia,re)
            reallistaupdate = []
            reallistaupdate.append(realtupla1)
            
            stringainsertar = '''
            UPDATE personas SET 
            nombre = ?,
            apellido = ?, 
            sexo = ?, 
            fecha_nac = ?,
            nacionalidad = ?,
            estado = ?,
            telefono = ?, 
            correo = ?,
            latitud = ?,
            longitud = ?,
            provincia = ? 
            WHERE personas.cedula = ?
            '''
            
            cursor.executemany(stringainsertar,reallistaupdate)
            conexion.commit()
            playsound('Registro actualizado.wav')
            print 'Tu registro se ha actualizado correctamente'
            raw_input('Vas a volver al menu...')
            conexion.close()
            menu()
    
    # si llego hasta aqui es porque no se enconstro ningun registro con esa cedula
    print 'No se ha encontrado ningun registro con la cedula que has introducido'
    raw_input('....')
    menu()

def exportarcasoparticular():
    os.system('cls')
    os.system('color 4f')
    playsound('Introducecedula.wav')
    cedula_caso_particular= raw_input('Porfavor introduce la cedula para poder exportar los datos a HTML: ')
    
    conexion = sqlite3.connect('database')
    cursor = conexion.cursor()
    
    cursor.execute('SELECT * FROM personas')
    
    data = cursor.fetchall()
    
    
    for dataa in data:
        hh = str(dataa)
        cedula = dataa[0]
        datos = get_data_cedula2(cedula)
        foto = datos[5]
        aver = hh.find(cedula_caso_particular)
        if aver != -1:
            realstring = '''
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <title>{}</title>
            </head>
            <body> 
            <font face = "Verdana, Geneva, sans-serif" size = "4" color = "#210B61">
                    <center> <h3 >Caso de {}</h3> </center>
                </font>
                <font face = "Verdana, Geneva, sans-serif" size = "4">
                <p align = "center">
                <img src = "{}"><br><br>
                    <b>Cedula: </b>{}  <br>
                    <b>Nombre: </b>{}<br>
                    <b>Apellidos: </b>{}<br>
                    <b>Sexo: </b> {}<br>
                    <b>Fecha Nacimiento: </b>{} <br>
                    <b>Nacionalidad: </b>{} <br>
                    <b>Estado: </b>{}<br>
                    <b>Telefono: </b>{} <br>
                    <b>Correo: </b>{} <br>
                    <b>Latitud: </b>{} <br>
                    <b>Longitud: </b>{} <br>
                    <b>Provincia: </b>{} <br>
                </p>
            </font>
            </body>
            </html>
            '''.format(dataa[1],dataa[1],foto,dataa[0],dataa[1],dataa[2],dataa[3],dataa[4],dataa[5],dataa[6],dataa[7],dataa[8],dataa[9],dataa[10],dataa[11])
            stringnombre = 'Casode' + dataa[1] + '.html'
            h = open(stringnombre,'w')
            h.write(realstring)
            h.close()
            conexion.commit()
            conexion.close()
            playsound('ss.wav')
            print 'Se ha exportau su caso correctamente con el nombre de: casode'+dataa[1]+'.html'
            raw_input('presiona una tecla')
            menu()

    playsound('Noseencontromiembro.wav')
    raw_input('No se encontro ningun resultado con esta cedula')
    menu()

def quitar():
    # abrir en h el archivo pa' leerlo
    h = open('allcases.html').readlines()
    # sacamos la cantidad de caracteres que tiene, que a su vez es la ultima posicion +1
    capacidadmax = len(h)
    #  y desimos que la ultima y penultima posicion son espacios en blanco para borrarlas
    h[capacidadmax-1] = ' '
    h[capacidadmax-2] = ' '
    # luego abrimos de new pero ahora en modo escritura para poder meter nuestro codigo con el elemento quitado
    j = open('allcases.html','w')
    # con este magnifico metodo podemos convertir de list a string perfectamente
    macabron = ' '.join(h)
    j.write(macabron)
    j.close()

def evaluar(mm,dd):
    ano = 2020
    fecha_nacimiento = date(ano,mm,dd)

    if fecha_nacimiento.month == 3 and fecha_nacimiento.day >= 21 and fecha_nacimiento.day <= 30 or fecha_nacimiento.month == 4 and fecha_nacimiento.day >= 1 and fecha_nacimiento.day <=20:
        return "aries"
    
    elif fecha_nacimiento.month == 4 and fecha_nacimiento.day >= 21 and fecha_nacimiento.day <= 30 or fecha_nacimiento.month == 5 and  fecha_nacimiento.day >= 1 and fecha_nacimiento.day <=20:
        return "tauro"
    
    elif  fecha_nacimiento.month == 5 and fecha_nacimiento.day >= 21 and fecha_nacimiento.day <= 30 or fecha_nacimiento.month == 6 and  fecha_nacimiento.day >= 1 and fecha_nacimiento.day <=24:
        return  "geminis"

    elif  fecha_nacimiento.month == 6 and fecha_nacimiento.day >= 25 and fecha_nacimiento.day <= 30 or fecha_nacimiento.month == 7 and  fecha_nacimiento.day >= 1 and fecha_nacimiento.day <=22:
        return "cancer"
    
    elif  fecha_nacimiento.month == 7 and fecha_nacimiento.day >= 23 and fecha_nacimiento.day <= 30 or fecha_nacimiento.month == 8 and  fecha_nacimiento.day >= 1 and fecha_nacimiento.day <=23:
        return  "leo"

    elif fecha_nacimiento.month == 8 and fecha_nacimiento.day >= 24 and fecha_nacimiento.day <= 30 or fecha_nacimiento.month == 9 and  fecha_nacimiento.day >= 1 and fecha_nacimiento.day <=23:
        return  'virgo'
    elif fecha_nacimiento.month == 9 and fecha_nacimiento.day >= 24 and fecha_nacimiento.day <= 30 or fecha_nacimiento.month == 10 and  fecha_nacimiento.day >= 1 and fecha_nacimiento.day <=22:
        return  'libra'
    elif fecha_nacimiento.month == 10 and fecha_nacimiento.day >= 23 and fecha_nacimiento.day <= 30 or fecha_nacimiento.month == 11 and  fecha_nacimiento.day >= 1 and fecha_nacimiento.day <=22:
        return 'escorpio'
    elif fecha_nacimiento.month == 11 and fecha_nacimiento.day >= 22 and fecha_nacimiento.day <= 30 or fecha_nacimiento.month == 12 and  fecha_nacimiento.day >= 1 and fecha_nacimiento.day <=21:
        return 'sagitario'
    elif fecha_nacimiento.month == 12 and fecha_nacimiento.day >= 22 and fecha_nacimiento.day <= 30 or fecha_nacimiento.month == 1 and  fecha_nacimiento.day >= 1 and fecha_nacimiento.day <=19:
        return  'capricornio'
    elif fecha_nacimiento.month == 1 and fecha_nacimiento.day >= 20 and fecha_nacimiento.day <= 30 or fecha_nacimiento.month == 2 and  fecha_nacimiento.day >= 1 and fecha_nacimiento.day <=18:
        return  'acuario'
    elif fecha_nacimiento.month == 2 and fecha_nacimiento.day >= 19 and fecha_nacimiento.day <= 30 or fecha_nacimiento.month == 3 and  fecha_nacimiento.day >= 1 and fecha_nacimiento.day <=20:
        return  'piscis'

def exportartodosloscasos():
    
    conexion = sqlite3.connect('database')
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM personas')
    realdata = cursor.fetchall()
    esqueleto_del_codigo_html = '''
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <title>MAXIMO</title>
                <style>
                    *{
                        text-align: center;
                        font-family: 'Comic Sans MS';
                    }
                    h3,b {
                        color:#39BBEF;

                    }   
                </style>
            </head>
            <body> 
                   
        </body></html>'''
    
    quitar()
    for xs in realdata:
        dataperson = get_data_cedula2(xs[0])
        foto = dataperson[5]
        apertura = open('allcases.html','a')
        bloques_a_agregar_codigo_html = '''
                <h3>Caso de {}</h3><br>
                    <img src = "{}"><br>
                    <b>Cedula: </b>{}<br>
                    <b>Nombre: </b>{}<br>
                    <b>Apellidos: </b>{}<br>
                    <b>Sexo: </b>{}<br>
                    <b>Fecha Nacimiento: </b>{}<br>
                    <b>Nacionalidad: </b>{}<br>
                    <b>Estado: </b>{}<br>
                    <b>Telefono: </b>{}<br>
                    <b>Correo: </b>{}<br>
                    <b>Latitud: </b>{}<br>
                    <b>Longitud: </b>{}<br>
                    <b>Provincia: </b>{}<br>
                    '''.format(xs[1],foto,xs[0],xs[1],xs[2],xs[3],xs[4],xs[5],xs[6],xs[7],xs[8],xs[9],xs[10],xs[11])
        apertura.write(bloques_a_agregar_codigo_html)
        
        
    try:
        apertura.write('</body></html>')
    except UnboundLocalError:
        print 'no hay datos insertaos'
        raw_input()
        menu()
        
    
    apertura.close()
    conexion.commit()
    conexion.close()
    playsound('bb.wav')
    print 'Se han exportado todos los casos correctamente'
    raw_input()
    menu()

def vermapa():
    os.system('color 1f')
    # verificacion de si existe el archivo de la pagina web
    existencia = os.path.exists('mapacasos.html')
    
    # codigo htmlcssjs donde esta el codigo fuente de la pagina
    codigohtmlcssjs = '''
        
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <link rel="stylesheet" href="https://unpkg.com/leaflet@1.6.0/dist/leaflet.css" />
            <script src="https://unpkg.com/leaflet@1.6.0/dist/leaflet.js"></script>
            <style>
                #map{position: absolute; top: 0; bottom: 0;left: 0; right: 0;}
            </style>
            <title>The Real Map</title>
        </head>
        <body>
            <div id = "map"></div>
            

            <script>
                
                var map = L.map('map').setView([0,0],1);
                L.tileLayer('https://api.maptiler.com/maps/streets/{z}/{x}/{y}.png?key=36c0GPCuROaO7NIPqAdv',{
                    attribution: '<a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a>',


            }).addTo(map);
            var marker = []
    '''
    # parte final que se agrega luego de meter todas los puntos 
    codigohtmlcssjsrestante = '\n</script></body></html>'
    # si no existe se crea
    if existencia == False:
        existencia = True

        creacion = open('mapacasos.html','w')
        creacion.write(codigohtmlcssjs)

        creacion.write(codigohtmlcssjsrestante)
        creacion.close()
        
    conexion = sqlite3.connect('database')
    cursor = conexion.cursor()
  
    cursor.execute('SELECT latitud,longitud FROM personas')
    realdata = cursor.fetchall()
    conexion.commit()
    conexion.close()

    # proceso para quitar la ultima linea del codigo en html para poder meter el codigo
    # de los puntos del mapa
    r = open('mapacasos.html').readlines()
    
    capacidadmax = len(r)

    asd = open('mapacasos.html','w')
    r[capacidadmax - 1 ] = ' '
    macabron = ' '.join(r)
    asd.write(macabron)
    asd.close()
    codigoremplazo = ''
    cabronelevador = open('mapacasos.html','a')
    stringmode = open('mapacasos.html').read()
    iteradora = 0
    for xs in realdata:
        #usar r para leer
        
        
        hh = '\nmarker[{}] = L.marker([{},{}]).addTo(map);'.format(iteradora,xs[0],xs[1])
        cabronelevador.write(hh)
        iteradora = iteradora + 1
        
    

    cabronelevador.write(codigohtmlcssjsrestante)
    cabronelevador.close()

    playsound('positivo.wav')
    print 'Se ha exportado correctamente su mapa!'
    raw_input('...')
    os.popen('mapacasos.html')
    menu()

def verificarsignos(signo):
    global diccionariossignos
    if signo == 'aries':
        diccionariossignos['aries'] += 1
    elif signo == 'tauro':
        diccionariossignos['tauro'] += 1
    elif signo == 'geminis':
        diccionariossignos['geminis'] += 1   
    elif signo == 'cancer':
        diccionariossignos['cancer'] += 1 
    elif signo == 'leo':
        diccionariossignos['leo'] += 1
    elif signo == 'virgo':
        diccionariossignos['virgo'] += 1
    elif signo == 'libra':
        diccionariossignos['libra'] += 1
    elif signo == 'escorpio':
        diccionariossignos['escorpio'] += 1
    elif signo == 'sagitario':
        diccionariossignos['sagitario'] += 1    
    elif signo == 'capricornio':
        diccionariossignos['capricornio'] += 1
    elif signo == 'acuario':
        diccionariossignos['acuario'] += 1
    elif signo == 'piscis':
        diccionariossignos['piscis'] += 1
    else:
        print 'no tiene signo este' 

def estadisticamistica():
    global diccionariossignos
    diccionariossignos = {'aries':0,'tauro':0,'geminis':0,'cancer':0,'leo':0,'virgo':0,'libra':0,
    'escorpio':0,'sagitario':0,'capricornio':0,'acuario':0,'piscis':0 }
    conexion = sqlite3.connect('database')
    cursor = conexion.cursor()
    # obtenemos los datos de la database y los alamcenamos en realdata
    cursor.execute('SELECT * FROM personas')
    realdata = cursor.fetchall()
    conexion.commit()
    conexion.close()
    # recorremos la realdata con un bucle for
    for xs  in realdata:
        # sacamos el dato de la cedula
        cedulaactual = xs[0]
        

        # obtenemos los datos homogeneisados de la api que nos devuelde una tupla
        
        datosapi1 = get_data_cedula2(cedulaactual)
        # obtenemos mes y dia mediante sus posiciones
        mes = datosapi1[3]
        dia = datosapi1[4]
        # obtenemos el signo zodiacal con la funcion evaluar()
        signo_zodiacal = evaluar(mes,dia)
        # con el metodo verificarsignos() le sumamos a cada signo el
        verificarsignos(signo_zodiacal)

    flowimprimir = '''
    CANTIDAD DE INFECTADOS POR SIGNO ZODIACAL:
    Aries: {}    
    Tauro: {}
    Geminis: {}
    Cancer: {}
    Leo: {}
    Virgo: {}
    Libra: {}
    Escorpio: {}
    Sagitario: {}
    Capricornio: {}
    Acuario: {}
    Piscis: {}
    '''.format(diccionariossignos['aries'],diccionariossignos['tauro'],diccionariossignos['geminis'],diccionariossignos['cancer'],diccionariossignos['leo'],diccionariossignos['virgo'],diccionariossignos['libra'],diccionariossignos['escorpio'],diccionariossignos['sagitario'],diccionariossignos['capricornio'],diccionariossignos['acuario'],diccionariossignos['piscis'])
    playsound('esta.wav')
    print flowimprimir
    playsound('Volver al menu.wav')
    raw_input('vas a volver al menu!')
    menu()

def sendMessage(mensaje,userid):
    requests.post('https://api.telegram.org/bot1263610917:AAEtM4HXytYtsFu2v3uQ5xEhJpOd4_oA_KI/sendMessage',
    data={'chat_id': userid, 'text':mensaje})

def alertatelegram():
    os.system('cls')
    
    playsound('enviacasos_coronavirus.wav')
    print 'Primero debes enviar un mensaje al canal de telegram: Casos_Coronavirus_bot'
    
    url = 'https://api.telegram.org/bot1263610917:AAEtM4HXytYtsFu2v3uQ5xEhJpOd4_oA_KI/getUpdates'
    playsound('Buscar personasunidas.wav')
    print 'Ahora el programa procedera a buscar las personas que estan unidas al canal \nEsto dependera de su conexion a internet\n'
    response = requests.get(url)
    ja = json.loads(response.content.decode('utf-8'))
    cantidad_message = len(ja['result'])
    listanombres = []
    # anadimos los nombres a una lista con ayuda de este bucle
    for xs in range(0,cantidad_message):
        hh = ja['result'][xs]['message']['from']['first_name']
        listanombres.append(hh)
    
    # ahora eliminamos los nombres repetidos para tener una lista limpia y se los mostramos al usuario
    listalimpia = set(listanombres)

    for xs  in listalimpia:

        print '* ',xs

       
    # bucle para hallar el id del user
    playsound('Escribe nombretuyo.wav')
    print '\nPorfavor escribe el nombre tuyo respetando correctamente las mayusculas'
    nombre_user = raw_input()
    for xs in range(0,cantidad_message):
        if ja['result'][xs]['message']['from']['first_name'] == nombre_user:
            userid = ja['result'][xs]['message']['from']['id']
            break
    try:
        if userid == '0':
            playsound('Noseencontromiembro.wav')
            print 'No se encontro ningun miembro del bot con ese nombre'
            print 'Asegurate de que lo hayas introducido correctamente y tambien de que hallas mandado el mensaje al canal y reintenda de nuevo'
            raw_input()
            sys.exit()
    except UnboundLocalError:
        print 'no ingreso el nombre correctamente'
        raw_input('presione cualquier tecla pa continuar')
        menu()
    
        
    aaa = open('userid.txt','w')
    
    aaa.write(str(userid))
    aaa.close()
    playsound('Ya te has registrado.wav')
    print 'Perfecto ya te has registrado!'
    raw_input()
    menu()

def menu():
    os.system('cls')
    os.system('color 6f')
    os.system("mode con cols=50")
    playsound('Bienvenido al programa.wav')
    print '\n\nBienvenido al real del proyecto final'
    #playsound('Casos por numero.wav')
    print '''Elige:
    
    
    1.    Agregar Caso
    2.    Editar Caso
    3.    Mostrar Casos
    4.    Exportar un Caso Particular HTML
    5.    Exportar Todos los Casos HTML
    6.    Ver Mapa de los Casos
    7.    Estadistica Mistica
    8.    Salir
    
    '''
    respuesta = str(raw_input("Elige tu respuesta: "))
    print respuesta
    if respuesta == '1':
        agregar()

    elif respuesta == "2":
        editar()

    elif respuesta == "3":
        listado()

    elif respuesta == "4":
        exportarcasoparticular()

    elif respuesta == "5":
        exportartodosloscasos()

    elif respuesta == "6":
        vermapa()

    elif respuesta == "7":
        estadisticamistica()

    elif respuesta == '8':
        print 'tu programa va a salir...'
        playsound('Programavaasalir.wav')
        raw_input()
        sys.exit()
    else:
        menu()

aa = open('userid.txt').readlines()
if aa[0] != ' ':
    menu()
else:
    playsound('Registrarte telegram.wav')
    print 'antes que todo debes registrarte en telegram para que asi el programa pueda enviarte un aviso con cada nuevo caso'
    respuesta1 = raw_input('quieres registrarte para que asi te lleguen las alarmas de casos a telegram?(si o no)')
    if respuesta1 == 'si':
        alertatelegram()
    elif respuesta1 == 'no':
        menu()
    else:
        menu()
