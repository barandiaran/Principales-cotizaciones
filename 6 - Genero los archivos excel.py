import pandas as pd
from openpyxl import load_workbook

# Ruta del archivo CSV
csv_file = 'z4_Cargo_pre_cotizaciones_mensuales.csv'

# Ruta del archivo Excel
excel_file = 'C:/Users/baran/OneDrive/Público/CotizacionesMensuales.xlsx'

# Leer el archivo CSV, excluyendo la columna 'Ord'
df_csv = pd.read_csv(csv_file)
df_csv = df_csv.drop(columns=['Ord'])

# Cargar el archivo Excel existente
book = load_workbook(excel_file)

# Seleccionar la hoja donde quieres añadir los datos
sheet = book.active  # Puedes especificar la hoja por nombre, ej. book['Sheet1']

# Convertir los datos del DataFrame a una lista de listas
data = df_csv.values.tolist()

# Determinar la fila de inicio (14 en este caso)
start_row = 14
start_col = 1  # Columna A

# Escribir los datos del CSV en la hoja de cálculo manteniendo el formato
for row_idx, row_data in enumerate(data, start=start_row):
    for col_idx, cell_value in enumerate(row_data, start=start_col):
        sheet.cell(row=row_idx, column=col_idx, value=cell_value)

# Obtener la tabla por su nombre y actualizar su rango
table = sheet.tables['T_Tabla']
start_cell = table.ref.split(':')[0]  # Obtener la celda de inicio de la tabla
end_cell = table.ref.split(':')[1]  # Obtener la celda final actual de la tabla
end_row = sheet[end_cell].row + 1  # Incrementar una fila
end_column = sheet[end_cell].column_letter  # Mantener la misma columna

# Actualizar la referencia de la tabla
new_ref = f"{start_cell}:{end_column}{end_row}"
table.ref = new_ref

# Guardar el archivo Excel con los datos añadidos
book.save(excel_file)