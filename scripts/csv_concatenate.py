import pandas as pd
from unidecode import unidecode

def generate_csv():
    # List of years
    years = range(2008, 2023)

    # List to store all files
    lista_dfs = []

    for year in years:
        # File path
        csv_file_path = f'/home/orlando_linux/alura_challange/csv_site/despesa_ceaps_{year}.csv'
        
        # Reading CSV file with 'latin-1' encoding, semicolon as delimiter, and removal of the first line.
        try:
            data = pd.read_csv(csv_file_path, delimiter=';', encoding='utf-8', skiprows=1)
        except UnicodeDecodeError:
            data = pd.read_csv(csv_file_path, delimiter=';', encoding='latin-1', skiprows=1)
        
        # To create the DataFrame for the current year and add it to the list
        df = pd.DataFrame(data)
        lista_dfs.append(df)

    # Concatenating all DataFrames from the list into a single DataFrame
    df = pd.concat(lista_dfs, ignore_index=True)
    print(f"The DataFrame contains {len(df)} rows.")

    # Wrangling the DATA variable
    print("\nRemoving rows where the 'DATA' column is null:")
    total_rows_before = len(df)
    df_1 = df.dropna(subset=['DATA'])
    total_rows_after = len(df_1)
    removed_rows = total_rows_before - total_rows_after
    removed_rows_percentage = (removed_rows / total_rows_before) * 100
    print(f"Removed {removed_rows} rows, comprising {removed_rows_percentage:.2f}% of the total.")

    # Converting the 'DATA' column to datetime with the correct format 'day/month/year'
    try:
        df_1.loc[:, 'DATA'] = pd.to_datetime(df_1['DATA'], format='%d/%m/%Y', errors='coerce')
    except ValueError as e:
        print(f"Error converting 'DATA' column to datetime: {e}")

    # Handling NaT values
    num_errors = df_1['DATA'].isna().sum()
    print(f"Number of rows with errors after conversion: {num_errors}")

    # Removing rows with NaT values in the 'DATA' column
    df_2 = df_1.dropna(subset=['DATA'])

    # Modifying 'VALOR_REEMBOLSADO' column
    print("\nModifying 'VALOR_REEMBOLSADO' column:")
    df_2.loc[:, 'VALOR_REEMBOLSADO'] = df_2['VALOR_REEMBOLSADO'].str.replace('\r\n', '').str.replace(',', '.')
    df_2.loc[:, 'VALOR_REEMBOLSADO'] = df_2['VALOR_REEMBOLSADO'].astype(float)

    # Resetting Index
    df_3 = df_2.reset_index(drop=True)

    # Function to normalize names
    def normalize_name(name):
        return unidecode(name)

    # Applying the normalize_name function to the 'SENADOR' column
    df_3['SENADOR'] = df_3['SENADOR'].apply(normalize_name)


    print(df_3.info())

    #Create CSV
    df_3.to_csv('/home/orlando_linux/alura_challange/csv_gold/csv_info_clean.csv', index=False)


if __name__ == "__main__":
    generate_csv()
