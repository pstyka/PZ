import pandas as pd

# Wczytanie danych z plików CSV
df1 = pd.read_csv('csv/final_tabela1.csv')
df2 = pd.read_csv('csv/final_tabela2.csv')

# Zmiana nazw kolumn w df2, aby pasowały do df1
df2 = df2.rename(columns={'σ_meta_exp': 'σm', 'σ_para_exp': 'σp'})

# Usunięcie kolumny 'n' z df2
df2 = df2.drop(columns=['n'])

# Przekonwertowanie odpowiednich kolumn na float
df1['σm'] = pd.to_numeric(df1['σm'], errors='coerce')
df1['σp'] = pd.to_numeric(df1['σp'], errors='coerce')
df2['σm'] = pd.to_numeric(df2['σm'], errors='coerce')
df2['σp'] = pd.to_numeric(df2['σp'], errors='coerce')

# Merge na podstawie kolumn 'σm' oraz 'σp'
merged_df = pd.merge(df1, df2, on=['σm', 'σp'], how='outer', indicator=True)

# Liczenie zmergowanych wierszy
merged_rows = merged_df[merged_df['_merge'] == 'both']
merged_count = merged_rows.shape[0]

# Wyświetlanie zmergowanych wierszy
print("Merged rows:")
print(merged_rows)

# Sprawdzanie ile razy każdy wiersz z df2 został użyty w merge'u
df2_merge_counts = merged_rows.groupby(['σm', 'σp']).size().reset_index(name='merge_count')
print("Merge counts for df2 rows:")
print(df2_merge_counts)

# Identyfikacja wierszy, które się nie zmergowały (tylko w df1 lub tylko w df2)
df1_only = merged_df[merged_df['_merge'] == 'left_only']
df2_only = merged_df[merged_df['_merge'] == 'right_only']
merged = merged_rows

# Usunięcie kolumn używanych do merge'a
df1_only = df1_only.drop(columns=['_merge'])
df2_only = df2_only.drop(columns=['_merge'])
merged = merged.drop(columns=['_merge'])

# Połączenie wynikowych DataFrames, zachowanie kolejności kolumn z df1
result_df = pd.concat([merged, df1_only, df2_only], ignore_index=True)

# Dodanie numeracji do nowych wierszy na końcu
max_number = int(result_df['number'].max())
df2_only['number'] = range(max_number + 1, max_number + 1 + len(df2_only))

# Połączenie wynikowych DataFrames, zachowanie kolejności kolumn z df1 (ponownie)
result_df = pd.concat([merged, df1_only, df2_only], ignore_index=True)

# Zachowanie kolejności według 'number' z df1
result_df = result_df.sort_values(by='number')

# Reorganizacja kolumn, aby kolumny z df1 były na początku
df1_columns = [col for col in df1.columns if col in result_df.columns]
df2_columns = [col for col in df2.columns if col not in df1_columns]
result_df = result_df[df1_columns + df2_columns]

# Zapisanie wynikowego DataFrame do pliku CSV
result_df.to_csv('merged_result.csv', index=False)

print("Merged DataFrame has been saved to 'merged_result.csv'")
print(f"Number of merged rows: {merged_count}")
