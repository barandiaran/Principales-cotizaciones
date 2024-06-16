import pandas as pd
import numpy as np
import os

##
##
##  Graba dos archivos con la info del lapso definido a continuación
##  UrlPrint = 'C:/Users/baran/OneDrive/Cursos/Python/z_ExcelFiles/Cotizaciones/Cotizaciones_Diarios.txt'
##  UrlPromedioPrint = 'C:/Users/baran/OneDrive/Cursos/Python/z_ExcelFiles/Cotizaciones/Cotizaciones_Promedio.txt'
##
##

##
##  Espacio de variables
##

# Armado de la lista de combinaciones 'AAAAMM' necesarios para abrir
desde_mes = 1
desde_año = 2017
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

meses = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Setiembre','Octubre','Noviembre','Diciembre']
meses_nro = ['01','02','03','04','05','06','07','08','09','10','11','12']
años = ["2017", "2018", "2019", "2020", "2021", "2022"]
indice_mes = 0

url_pre = 'Cotizaciones_{}.xls'
url = ''

NroFila = 0
IdNroFila = 0

CantFilas = 0
CantColumnas = 0

Texto_año = ''
Texto_mes = ''
Texto_mes_pre = 0

##### Preparo la impresión
UrlPrint = 'z2_Cotizaciones_Diarios.txt'
UrlPromedioPrint = 'z2_Cotizaciones_Promedio.txt'
if os.path.exists(UrlPrint):
    os.remove(UrlPrint)
if os.path.exists(UrlPromedioPrint):
    os.remove(UrlPromedioPrint)

##
##  Espacio de instrucciones
##

for cadames in lista_meses:

    work_año = cadames[:4]
    work_mes = cadames[4:6]
    text_mes = meses[int(work_mes) - 1]
    url = url_pre.format(cadames)
    
    if os.path.exists(url):
        df = pd.read_excel(url)
        cantFilas = df.shape[0]
        cantColumnas = df.shape[1]
        for indice_fila, fila in df.iterrows():
            if fila[1] == 'Día':
                NroFila = indice_fila
        # print('Cotizaciones{} - {}'.format(cadames, NroFila))

        NroFila -= 1
        if pd.isna(df.values[NroFila, 1]):
            NroFila -= 1   
        Texto_año = str(df.values[NroFila, 1])
        NroFila -= 1
        Texto_mes_pre = meses.index(df.values[NroFila, 1].strip())
        Texto_mes = str(meses_nro[Texto_mes_pre])

        print("{}{}".format(Texto_año, Texto_mes))
        print("{}".format(cadames))

        titulos = []

        # titulos.append("{}{}".format(Texto_año, Texto_mes))
        titulos.append("DIA")
        
        for i in range(2, cantColumnas):
            mitexto = "{} {}".format(df.values[NroFila, i], df.values[NroFila + 1, i])
            mitexto = mitexto.replace(' nan', '')
            titulos.append(mitexto)

        NroFila += 3

        # Imprimo los títulos en el archivo .txt
        if not os.path.exists(UrlPrint):
            with open(UrlPrint, 'w') as temp_file:
                for item in titulos:
                    temp_file.write("%s;" % item)
                temp_file.write('\n')
        if not os.path.exists(UrlPromedioPrint):
            with open(UrlPromedioPrint, 'w') as temp_file:
                for item in titulos:
                    temp_file.write("%s;" % item)
                temp_file.write('\n')

        ##  Armo el cuadro de los valores de cada dia

        for i in range(NroFila, cantFilas - 1):
            if isinstance(df.values[i, 1], int):
                if df.values[i, 1] <= 35:
                    mifecha = "{}{}{}".format(Texto_año, Texto_mes, f'{df.values[i, 1]:02d}')
                    milinea = []
                    milinea.append(mifecha)
                    for j in range(2, cantColumnas):
                        milinea.append(df.values[i, j])
                    print(milinea)

                    # Imprimo cada linea en el archivo .txt
                    with open(UrlPrint, 'a') as temp_file:
                        for item in milinea:
                            temp_file.write("%s;" % str(item).replace('.',','))
                        temp_file.write('\n')
        
        ##  Armo el cuadro de los valores mensuales promedio

        for i in range(NroFila, cantFilas - 1):
            if df.values[i, 1] == "PROMEDIO":
                nrofila_prom = i

        mifecha = "{}{}".format(Texto_año, Texto_mes)
        milinea = []
        milinea.append(mifecha)
        for j in range(2, cantColumnas):
            milinea.append(df.values[nrofila_prom, j])
        print(milinea)

        # Imprimo la linea del promedio en el archivo promedio .txt
        with open(UrlPromedioPrint, 'a') as temp_file:
            for item in milinea:
                temp_file.write("%s;" % str(item).replace('.',','))
            temp_file.write('\n')

    else: 
        print('Archivo no existe - cotizaciones{}'.format(cadames))


