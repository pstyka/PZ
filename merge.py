import pandas as pd


df1 = pd.read_csv('combined_tabela.csv')
df2 = pd.read_csv('combined_new_tabela.csv')


df2 = df2.rename(columns={'σ_meta_exp': 'σm', 'σ_para_exp': 'σp'})


df2 = df2.drop(columns=['n'])


df1['σm'] = pd.to_numeric(df1['σm'], errors='coerce')
df1['σp'] = pd.to_numeric(df1['σp'], errors='coerce')
df2['σm'] = pd.to_numeric(df2['σm'], errors='coerce')
df2['σp'] = pd.to_numeric(df2['σp'], errors='coerce')


merged_df = pd.merge(df1, df2, on=['σm', 'σp'], how='outer', indicator=True)


df1_only = merged_df[merged_df['_merge'] == 'left_only']
df2_only = merged_df[merged_df['_merge'] == 'right_only']
merged = merged_df[merged_df['_merge'] == 'both']


df1_only = df1_only.drop(columns=['_merge'])
df2_only = df2_only.drop(columns=['_merge'])
merged = merged.drop(columns=['_merge'])


result_df = pd.concat([merged, df1_only, df2_only], ignore_index=True)


result_df = result_df.sort_values(by='number')


df1_columns = [col for col in df1.columns if col in result_df.columns]
df2_columns = [col for col in df2.columns if col not in df1_columns]
result_df = result_df[df1_columns + df2_columns]


result_df.to_csv('merged_result.csv', index=False)

print("Merged DataFrame has been saved to 'merged_result.csv'")
