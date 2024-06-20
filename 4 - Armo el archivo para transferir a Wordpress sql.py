##
##  Tengo que convertir el archivo "CotizacionesMensuales_ok.csv" en el 
##  archivo que me va a cargar la tabla "cotizaciones_mensuales" en la base de datos
##  de Wordpress u964613875_Datos
##  
##

import pandas as pd

# Cargar el archivo CSV original
file_path = 'z3_CotizacionesMensuales_ok.csv'
df = pd.read_csv(file_path)

# Renombrar la columna 'Euro' a 'Euro2'
df.rename(columns={'Euro': 'Euro2'}, inplace=True)

# Diccionario para convertir número de mes a nombre abreviado en español
meses = {
    1: "Ene",
    2: "Feb",
    3: "Mar",
    4: "Abr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Ago",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dic"
}

# Crear la columna 'Ord' con valores incrementales
# df['Ord'] = range(1, len(df) + 1)
df['Ord'] = range(len(df), 0, -1)

# Crear la columna 'mMes'
df['mMes'] = df.apply(lambda row: f"{meses[row['Mes']]}-{str(row['Año'])[-2:]}", axis=1)

# Crear la columna 'UltDia'
df['UltDia'] = df.apply(lambda row: f"{row['Año']}-{str(row['Mes']).zfill(2)}-{str(row['Día']).zfill(2)}", axis=1)

# Crear la columna 'Dolar' y formatear los valores con tres decimales
df['Dolar'] = df['Dolar cierre (*)'].apply(lambda x: f"{float(str(x).replace(',', '.')):.3f}".replace('.', ','))

# Crear la columna 'Dol_fondo' y formatear los valores con tres decimales
df['Dol_fondo'] = df['Dolar fondo (**)'].apply(lambda x: f"{float(str(x).replace(',', '.')):.3f}".replace('.', ','))

# Crear la columna 'Dol_prom' y formatear los valores con tres decimales
df['Dol_prom'] = df['Dolar prom (*)'].apply(lambda x: f"{float(str(x).replace(',', '.')):.3f}".replace('.', ','))

# Crear la columna 'Arg' y formatear los valores con tres decimales
df['Arg'] = df['Arg. $ (*)'].apply(lambda x: f"{float(str(x).replace(',', '.')):.3f}".replace('.', ','))

# Crear la columna 'BReal' y formatear los valores con tres decimales
df['BReal'] = df['Real (*)'].apply(lambda x: f"{float(str(x).replace(',', '.')):.3f}".replace('.', ','))

# Crear la columna 'Euro' y formatear los valores con tres decimales
df['Euro'] = df['Euro2'].apply(lambda x: f"{float(str(x).replace(',', '.')):.3f}".replace('.', ','))

# Crear la columna 'Oro' y formatear los valores con dos decimales
df['Oro'] = df['Oro Londres (***)'].apply(lambda x: f"{float(str(x).replace(',', '.')):.2f}".replace('.', ','))

# Eliminar las columnas originales
columns_to_drop = ['Año', 'Mes', 'Día', 'Arg. $ (*)', 'Real (*)', 'Dolar cierre (*)', 'Dolar fondo (**)', 'Dolar prom (*)', 'Euro2', 'Oro Londres (***)']
df.drop(columns=columns_to_drop, inplace=True)

# Guardar el DataFrame modificado en un nuevo archivo CSV
output_file_path = 'z4_Cargo_pre_cotizaciones_mensuales.csv'
df.to_csv(output_file_path, index=False)

print(f"Archivo guardado en: {output_file_path}")
