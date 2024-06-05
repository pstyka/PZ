import pandas as pd

# Wczytanie danych z plików CSV
df1 = pd.read_csv('csv/final_tabela1.csv')

# Przekonwertowanie odpowiednich kolumn na float
df1['σm'] = pd.to_numeric(df1['σm'], errors='coerce')
df1['σp'] = pd.to_numeric(df1['σp'], errors='coerce')

# Sprawdzanie, czy wiersze w df1 mają takie same wartości w kolumnach 'σm' i 'σp'
duplicate_rows_df1 = df1[df1.duplicated(subset=['σm', 'σp'], keep=False)]

if not duplicate_rows_df1.empty:
    print("Duplicate rows in df1 based on 'σm' and 'σp':")
    print(duplicate_rows_df1)
else:
    print("No duplicate rows in df1 based on 'σm' and 'σp'.")

# Jeśli potrzebujesz zapisać wyniki do pliku CSV
duplicate_rows_df1.to_csv('duplicate_rows_df1.csv', index=False)
