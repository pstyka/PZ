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


def clean_and_split_dataframe(df, expected_columns):
    print("Cleaning and splitting dataframe...")
    print("Current columns:", df.columns.tolist())

    num_columns = len(expected_columns)

    if len(df.columns) == num_columns * 2:
        part1_df = df.iloc[:, :num_columns].copy()
        part2_df = df.iloc[:, num_columns:].copy()

        part1_df.columns = expected_columns
        part2_df.columns = expected_columns

        part1_df = part1_df.dropna(how='all')
        part2_df = part2_df.dropna(how='all')

        part1_df = part1_df[pd.to_numeric(part1_df['n'], errors='coerce').notnull()]
        part2_df = part2_df[pd.to_numeric(part2_df['n'], errors='coerce').notnull()]

        combined_cleaned_df = pd.concat([part1_df, part2_df], ignore_index=True)
        print(f"Combined cleaned dataframe has {len(combined_cleaned_df)} rows")
        return combined_cleaned_df
    else:
        print(f"Unexpected number of columns: {len(df.columns)}.")
        return pd.DataFrame()


def save_dataframe_to_csv(df, csv_path):
    df.to_csv(csv_path, index=False)
    print(f"Data saved to {csv_path}")


if __name__ == "__main__":
    pdf_path = 'pdf/tabela2.pdf'
    pages = '4'
    combined_csv_path = 'csv/final_tabela2.csv'


    expected_columns = ["n", "SMILES", "σ_meta_exp", "σ_meta_calc", "σ_para_exp", "σ_para_calc"]


    combined_df = extract_tables_from_pdf(pdf_path, pages, flavor='stream')

    if not combined_df.empty:

        final_df = clean_and_split_dataframe(combined_df, expected_columns)

        if not final_df.empty:

            save_dataframe_to_csv(final_df, combined_csv_path)
        else:
            print("Final dataframe is empty after cleaning and splitting.")
    else:
        print("No data extracted from the PDF.")
