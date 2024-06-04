import camelot
import pandas as pd


def extract_tables_from_pdf(pdf_path, pages, flavor='stream'):
    print(f"Extracting tables from pages: {pages} using flavor: {flavor}")
    tables = camelot.read_pdf(pdf_path, pages=pages, flavor=flavor)

    if tables.n == 0:
        print(f"No tables found on pages: {pages}")
        return pd.DataFrame()

    combined_df = pd.concat([table.df for table in tables])
    combined_df.columns = combined_df.iloc[0]
    combined_df = combined_df[1:]
    combined_df.reset_index(drop=True, inplace=True)

    print(f"Extracted {len(combined_df)} rows from pages: {pages}")
    return combined_df


def clean_dataframe(df, expected_columns):
    print("Cleaning dataframe...")
    print("Current columns:", df.columns.tolist())

    if len(df.columns) == len(expected_columns):
        df.columns = expected_columns
    else:
        print(f"Unexpected number of columns: {len(df.columns)}. Adjusting headers accordingly.")
        for i in range(len(df.columns)):
            if i < len(expected_columns):
                df = df.rename(columns={df.columns[i]: expected_columns[i]})
            else:
                df = df.drop(df.columns[i], axis=1)

    df = df.dropna(how='all')

    print(f"Cleaned dataframe has {len(df)} rows")
    return df


def save_dataframe_to_csv(df, csv_path):
    df.to_csv(csv_path, index=False)
    print(f"Data saved to {csv_path}")


if __name__ == "__main__":
    pdf_path = 'pdfik2.pdf'
    pages = '4'
    combined_csv_path = 'combined_new_tabela.csv'


    combined_df = extract_tables_from_pdf(pdf_path, pages, flavor='stream')

    if not combined_df.empty:

        num_columns = combined_df.shape[1] // 2


        expected_columns_part1 = ["n", "SMILES", "σ_meta_exp", "σ_meta_calc", "σ_para_exp", "σ_para_calc"]
        expected_columns_part2 = ["n", "SMILES", "σ_meta_exp", "σ_meta_calc", "σ_para_exp", "σ_para_calc"]


        part1_df = combined_df.iloc[:, :num_columns].copy()
        part2_df = combined_df.iloc[:, num_columns:].copy()


        cleaned_df_part1 = clean_dataframe(part1_df, expected_columns_part1)
        cleaned_df_part2 = clean_dataframe(part2_df, expected_columns_part2)


        cleaned_df_part2.columns = [f"{col}_part2" for col in cleaned_df_part2.columns]

        final_df = pd.concat([cleaned_df_part1, cleaned_df_part2], axis=1)

        save_dataframe_to_csv(final_df, combined_csv_path)
    else:
        print("No data extracted from the PDF.")
