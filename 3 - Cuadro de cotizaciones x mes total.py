##
##  Abro el diario de cotizaciones y busco el cierre de fin de mes
##  Luego de encontrar el último día, busco el promedio en el de cotizaciones promedio
##  Diarios 'Cotizaciones_Diarios.txt'
##  Promedi 'Cotizaciones_Promedio.txt'
##

import pandas as pd

# Ruta de los archivos
pre_path = ''
## Archivos fuente de información
file_diarios_path = pre_path + 'z2_Cotizaciones_Diarios.txt'
file_promedio_path = pre_path + 'z2_Cotizaciones_Promedio.txt'
## Archivos destino
output_file_path = pre_path + 'z3_CotizacionesMensuales.csv'
archivo_nuevo = pre_path + "z3_CotizacionesMensuales_ok.csv" 

# Leer los archivos de texto en DataFrames, especificando el separador ';' y la codificación 'latin1'
df_diarios = pd.read_csv(file_diarios_path, sep=";", encoding='latin1')
df_promedio = pd.read_csv(file_promedio_path, sep=";", encoding='latin1')

# Convertir la columna 'DIA' a formato de fecha en df_diarios
df_diarios['DIA'] = pd.to_datetime(df_diarios['DIA'], format='%Y%m%d')

# Crear una nueva columna 'AñoMes' en df_diarios con el formato 'AñoMes'
df_diarios['AñoMes'] = df_diarios['DIA'].dt.strftime('%Y%m')

# Crear una nueva columna 'AñoMes' en df_promedio con el formato 'AñoMes'
df_promedio['AñoMes'] = pd.to_datetime(df_promedio['DIA'], format='%Y%m').dt.strftime('%Y%m')

# Extraer el último día de cada mes de df_diarios
df_diarios['year_month'] = df_diarios['DIA'].dt.to_period('M')
last_day_of_month = df_diarios.groupby('year_month')['DIA'].transform(max) == df_diarios['DIA']
cotizaciones_mensuales = df_diarios[last_day_of_month].copy()

# Eliminar la columna 'year_month' que solo era necesaria para el cálculo
cotizaciones_mensuales = cotizaciones_mensuales.drop(columns=['year_month'])

# Separar la columna 'DIA' en 'Año', 'Mes' y 'Día'
cotizaciones_mensuales['Año'] = cotizaciones_mensuales['DIA'].dt.year.astype(str)
cotizaciones_mensuales['Mes'] = cotizaciones_mensuales['DIA'].dt.month.astype(str).str.zfill(2)
cotizaciones_mensuales['Día'] = cotizaciones_mensuales['DIA'].dt.day.astype(str).str.zfill(2)

# Unir los DataFrames en función de la columna 'AñoMes'
cotizaciones_mensuales = cotizaciones_mensuales.merge(df_promedio[['AñoMes', 'Dólar USA* Billete']], on='AñoMes', how='left')

# Renombrar la nueva columna para evitar confusión
cotizaciones_mensuales.rename(columns={'Dólar USA* Billete': 'Dólar USA Promedio'}, inplace=True)

# Reordenar las columnas para tener 'Año', 'Mes', 'Día' al principio
cols = ['Año', 'Mes', 'Día'] + [col for col in cotizaciones_mensuales.columns if col not in ['Año', 'Mes', 'Día', 'AñoMes']]
cotizaciones_mensuales = cotizaciones_mensuales[cols]

# Guardar la nueva tabla en un archivo CSV
cotizaciones_mensuales.to_csv(output_file_path, index=False)

###  ORDENAMIENTO

# Eliminar las columnas "DIA" y "Unnamed: 7"
cotizaciones_mensuales = cotizaciones_mensuales.drop(columns=["DIA", "Unnamed: 7"])

# Cambiar los nombres de las columnas
cotizaciones_mensuales = cotizaciones_mensuales.rename(columns={
    "Peso Argentino * Billete": "Arg. $ (*)",
    "Real* Billete": "Real (*)",
    "Dólar USA* Billete_x": "Dolar cierre (*)",
    "Dólar USA* Fondo BCU": "Dolar fondo (**)",
    "Euro*": "Euro",
    "Oro Londres (en Dolares)": "Oro Londres (***)",
    "Dólar USA* Billete_y": "Dolar prom (*)"
})

# Reordenar las columnas para que "Dolar prom (*)" esté después de "Dolar fondo (**)"
columnas_ordenadas = [
    "Año", "Mes", "Día", "Arg. $ (*)", "Real (*)", "Dolar cierre (*)", 
    "Dolar fondo (**)", "Dolar prom (*)", "Euro", "Oro Londres (***)"
]
cotizaciones_mensuales = cotizaciones_mensuales[columnas_ordenadas]

# Guardar el archivo con el nuevo nombre
cotizaciones_mensuales.to_csv(archivo_nuevo, index=False)

print(f"Archivo guardado como {archivo_nuevo}")