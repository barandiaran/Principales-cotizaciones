from urllib import request
from urllib import error
import os

##
## Espacio de variables
##

# Armado de la lista de combinaciones 'AAAAMM' necesarios para abrir
desde_mes = 5           ## Dato ingresado
desde_año = 2024        ## Dato ingresado
hasta_mes = 12          ## Dato ingresado
hasta_año = 2024        ## Dato ingresado
work_mes = 0
text_mes = 'Enero'
work_año = 0
lista_meses = []

desde_añomes = "{}{}".format(str(desde_año), str(desde_mes).rjust(2, '0'))
hasta_añomes = "{}{}".format(str(hasta_año), str(hasta_mes).rjust(2, '0'))
work_añomes = desde_añomes

while work_añomes <= hasta_añomes:
    lista_meses.append(work_añomes)
    work_año = int(work_añomes[:4])
    work_mes = int(work_añomes[4:6])
    if work_mes == 12:
        work_mes = 1
        work_año += 1
    else:
        work_mes += 1
    work_añomes = "{}{}".format(str(work_año), str(work_mes).rjust(2, '0'))

## Otras variables

existe_archivo = False
sobreescribir_archivos = False     ## IMPORTANTE  Si True entonces sobreescribirá los archivos por lo que las correcciones se borrarán

meses = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Setiembre','Octubre','Noviembre','Diciembre']
meses_nro = ['01','02','03','04','05','06','07','08','09','10','11','12']
años = ["2017", "2018", "2019", "2020", "2021", "2022"]

url_pre = "https://www.bcu.gub.uy/Estadisticas-e-Indicadores/Promedio%20Mensual%20de%20Arbitrajes/Principales%20cotizaciones%20-%20{}%20{}.xls"
url = "" 

## Archivo destino
nombrarch_pre = 'Cotizaciones_{}.xls'
nombrarch = ""

for cadames in lista_meses:
    work_año = cadames[:4]
    work_mes = cadames[4:6]
    text_mes = meses[int(work_mes) - 1]
    url = url_pre.format(meses[int(work_mes) - 1], work_año)

    try:
        nombrarch = nombrarch_pre.format(cadames)
        # Busco si ya bajé este archivo
        existe_archivo = os.path.isfile(nombrarch)

        if not existe_archivo:
            request.urlretrieve(url, nombrarch)
            print('{}{} - ok!'.format(work_año, work_mes))
        else:
            if sobreescribir_archivos:
                request.urlretrieve(url, nombrarch)
                print('{}{} - actualizado ok!'.format(work_año, work_mes))               
            else:
                print('{}{} existe. No se actualizó'.format(work_año, work_mes))            
    except error.HTTPError as e:
        if e.code ==  404:
            print("Archivo no encontrado -> Mes : {} - {}".format(work_año, work_mes))
        

'''
# Las páginas para sacar los datos es la siguiente
# https://www.bcu.gub.uy/Estadisticas-e-Indicadores/Paginas/Promedio-Mensual-de-Arbitrajes.aspx

'''