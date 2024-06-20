import pandas as pd

def generate_sql_from_csv(csv_path, table_name):
    # Load the CSV file
    data = pd.read_csv(csv_path)

    # Function to replace commas with dots in decimal values
    def replace_commas(value):
        if isinstance(value, str):
            return value.replace(',', '.')
        return value

    # Start SQL script with truncate statement
    sql_script = f"TRUNCATE TABLE {table_name};\n\n"

    # Prepare the insert statement prefix
    insert_prefix = f"INSERT INTO {table_name} (Ord, mMes, UltDia, Dolar, Dol_fondo, Dol_prom, Arg, BReal, Euro, Oro)\nVALUES\n"

    # Generate the SQL insert statements for each row in the CSV
    insert_statements = []
    for _, row in data.iterrows():
        values = tuple(replace_commas(value) for value in row)
        insert_statement = f"('{values[0]}', '{values[1]}', '{values[2]}', '{values[3]}', '{values[4]}', '{values[5]}', '{values[6]}', '{values[7]}', '{values[8]}', '{values[9]}')"
        insert_statements.append(insert_statement)

    # Join all insert statements into one SQL command
    sql_insert = ",\n".join(insert_statements) + ";"
    sql_script += insert_prefix + sql_insert

    return sql_script

# Define the path to the CSV file and the table name
csv_path = 'z4_Cargo_pre_cotizaciones_mensuales.csv'
table_name = 'cotizaciones_mensuales'

# Generate the SQL script
sql_script = generate_sql_from_csv(csv_path, table_name)

# Save the SQL script to a file
output_file_path = 'z5_cotizaciones_mensuales_insert.sql'
with open(output_file_path, 'w') as file:
    file.write(sql_script)

# Lo copio en c:\Users\baran\OneDrive\Público para su importación desde phpadmin
output_file_path = 'c:/Users/baran/OneDrive/Público/z5_cotizaciones_mensuales_insert.sql'
with open(output_file_path, 'w') as file:
    file.write(sql_script)

print(f"SQL script generated and saved to {output_file_path}")
