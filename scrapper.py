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


def clean_dataframe(df):
    print("Cleaning dataframe...")
    print("Current columns:", df.columns.tolist())

    expected_columns = ["number", "substituent", "σm", "σp", "F", "R", "References"]

    if len(df.columns) == 7:
        df.columns = expected_columns
    else:
        print(f"Unexpected number of columns: {len(df.columns)}. Adjusting headers accordingly.")
        for i in range(len(df.columns)):
            if i < len(expected_columns):
                df.rename(columns={df.columns[i]: expected_columns[i]}, inplace=True)
            else:
                df.drop(df.columns[i], axis=1, inplace=True)

    df['substituent'] = ""

    df['number'] = df['number'].str.replace('.', '', regex=False)
    df = df[pd.to_numeric(df['number'], errors='coerce').notnull()]
    df.loc[:, 'number'] = df['number'].astype(int)
    df = df[df['number'].between(1, 530)]
    df = df.dropna(how='all')

    print(f"Cleaned dataframe has {len(df)} rows")
    return df


def save_dataframe_to_csv(df, csv_path):
    df.to_csv(csv_path, index=False)
    print(f"Data saved to {csv_path}")


if __name__ == "__main__":
    pdf_path = 'pdfik.pdf'
    main_pages = '1-7'
    last_page = '8'
    main_csv_path = 'tabela1.csv'
    last_page_csv_path = 'tabela_last_page.csv'
    combined_csv_path = 'combined_tabela.csv'
    substituents_csv_path = 'substituents1.csv'

    combined_df_main = extract_tables_from_pdf(pdf_path, main_pages, flavor='stream')
    combined_df_last_page = extract_tables_from_pdf(pdf_path, last_page, flavor='stream')

    if not combined_df_main.empty:
        cleaned_df_main = clean_dataframe(combined_df_main)
        unique_df_main = cleaned_df_main.drop_duplicates(subset='number', keep='first')
        save_dataframe_to_csv(unique_df_main, main_csv_path)
    else:
        print("No data extracted from the main pages.")

    if not combined_df_last_page.empty:
        print("Last page columns before cleaning:", combined_df_last_page.columns.tolist())
        print("Last page data preview:")
        print(combined_df_last_page.head())

        cleaned_df_last_page = clean_dataframe(combined_df_last_page)
        unique_df_last_page = cleaned_df_last_page.drop_duplicates(subset='number', keep='first')
        save_dataframe_to_csv(unique_df_last_page, last_page_csv_path)
    else:
        print("No data extracted from the last page.")

    # Load the main and substituents CSV files
    main_df = pd.read_csv(main_csv_path)
    substituents_df = pd.read_csv(substituents_csv_path)

    # Merge the substituents into the main dataframe based on 'number'
    merged_df = pd.merge(main_df, substituents_df, on='number', how='left')

    # Drop the old 'substituent' column and rename the new one
    merged_df.drop(columns=['substituent_x'], inplace=True)
    merged_df.rename(columns={'substituent_y': 'substituent'}, inplace=True)

    # Reorder columns to make 'substituent' the second column
    columns_order = ['number', 'substituent', 'σm', 'σp', 'F', 'R', 'References']
    merged_df = merged_df[columns_order]

    # Save the combined dataframe to a new CSV file
    save_dataframe_to_csv(merged_df, combined_csv_path)
