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
    df.dropna(subset=['DATA'], inplace = True) 
    print(f"Dataframe now contains {len(df)} rows.")

    # Converting the 'DATA' column to datetime with the correct format 'day/month/year'
    try:
        df['DATA'] = pd.to_datetime(df['DATA'], format='%d/%m/%Y', errors='coerce')
        df.dropna(subset=['DATA'], inplace=True)  # Removing rows with NaT values after conversion
    except ValueError as e:
        print(f"Error converting 'DATA' column to datetime: {e}")

    # Handling NaT values
    print(f"Number of rows with errors after conversion: {df['DATA'].isna().sum()}")

    # Modifying 'VALOR_REEMBOLSADO' column
    print("\nModifying 'VALOR_REEMBOLSADO' column:")
    df['VALOR_REEMBOLSADO'] = df['VALOR_REEMBOLSADO'].str.replace('\r\n', '').str.replace(',', '.')
    df['VALOR_REEMBOLSADO'] = df['VALOR_REEMBOLSADO'].astype(float)

    # Resetting Index
    df = df.reset_index(drop=True)

    # Correct names function
    def correct_names_in_dataframe(df, column_name):
        corrections = {
            'A�CIO NEVES': 'AÉCIO NEVES',
            'ANA AM�LIA': 'ANA AMÉLIA',
            '�NGELA PORTELA': 'ÂNGELA PORTELA',
            'AN�BAL DINIZ': 'ANÍBAL DINIZ',
            'ANT�NIO CARLOS VALADARES': 'ANTÔNIO CARLOS VALADARES',
            'ATA�DES OLIVEIRA': 'ATAÍDES OLIVEIRA',
            'C�SSIO CUNHA LIMA': 'CÁSSIO CUNHA LIMA',
            'C�CERO LUCENA': 'CÍCERO LUCENA',
            'D�RIO BERGER': 'DÁRIO BERGER',
            'EDISON LOB�O': 'EDISON LOBÃO',
            'ELMANO F�RRER': 'ELMANO FÉRRER',
            'EPIT�CIO CAFETEIRA': 'EPITÁCIO CAFETEIRA',
            'F�TIMA BEZERRA': 'FÁTIMA BEZERRA',
            'H�LIO JOS�': 'HÉLIO JOSÉ',
            'IN�CIO ARRUDA': 'INÁCIO ARRUDA',
            'JO�O ALBERTO SOUZA': 'JOÃO ALBERTO SOUZA',
            'JO�O CAPIBERIBE': 'JOÃO CAPIBERIBE',
            'JO�O DURVAL': 'JOÃO DURVAL',
            'JO�O VICENTE CLAUDINO': 'JOÃO VICENTE CLAUDINO',
            'JOS� AGRIPINO': 'JOSÉ AGRIPINO',
            'JOS� MARANH�O': 'JOSÉ MARANHÃO',
            'JOS� MEDEIROS': 'JOSÉ MEDEIROS',
            'JOS� PIMENTEL': 'JOSÉ PIMENTEL',
            'JOS� SERRA': 'JOSÉ SERRA',
            'L�DICE DA MATA': 'LÍDICE DA MATA',
            'L�CIA V�NIA': 'LÚCIA VÂNIA',
            'MARCO ANT�NIO COSTA': 'MARCO ANTÔNIO COSTA',
            'M�RIO COUTO': 'MÁRIO COUTO',
            'RICARDO FERRA�O': 'RICARDO FERRAÇO',
            'ROBERTO REQUI�O': 'ROBERTO REQUIÃO',
            'ROM�RIO': 'ROMÁRIO',
            'ROMERO JUC�': 'ROMERO JUCÁ',
            'RUBEN FIGUEIR�': 'RUBEN FIGUEIRÓ',
            'S�RGIO PETEC�O': 'SÉRGIO PETECÃO',
            'SODR� SANTORO': 'SODRÉ SANTORO',
            'TELM�RIO MOTA': 'TELMÁRIO MOTA',
            'ZEZ� PERRELLA': 'ZEZÉ PERRELLA'
             }
    
        df[column_name] = df[column_name].apply(lambda x: corrections.get(x, x))

    #Applying the normalize_name function to the 'SENADOR' column
    correct_names_in_dataframe(df,'SENADOR')


    print(df.info())

    # Convert 'Month' and 'Year' columns to strings and concatenate them
    df['Month-Year'] = df['ANO'].astype(str) + '-' + df['MES'].astype(str)

    # Convert the concatenated string to datetime format
    df['Month-Year'] = pd.to_datetime(df['Month-Year'], format='%Y-%m')

    def correct_tipo_despesa(df):
        corrections = {
            'Aluguel de im�veis para escrit�rio pol�tico, compreendendo despesas concernentes a eles.': 'Aluguel de imóveis para escritório político, compreendendo despesas concernentes a eles.',
            'Divulga��o da atividade parlamentar': 'Divulgação da atividade parlamentar',
            'Locomo��o, hospedagem, alimenta��o, combust�veis e lubrificantes': 'Locomoção, hospedagem, alimentação, combustíveis e lubrificantes',
            'Contrata��o de consultorias, assessorias, pesquisas, trabalhos t�cnicos e outros servi�os de apoio ao exerc�cio do mandato parlamentar': 'Contratação de consultorias, assessorias, pesquisas, trabalhos técnicos e outros serviços de apoio ao exercício do mandato parlamentar',
            'Aquisi��o de material de consumo para uso no escrit�rio pol�tico, inclusive aquisi��o ou loca��o de software, despesas postais, aquisi��o de publica��es, loca��o de m�veis e de equipamentos. ': 'Aquisição de material de consumo para uso no escritório político, inclusive aquisição ou locação de software, despesas postais, aquisição de publicações, locação de móveis e de equipamentos.',
            'Passagens a�reas, aqu�ticas e terrestres nacionais': 'Passagens aéreas, aquáticas e terrestres nacionais',
            'Servi�os de Seguran�a Privada': 'Serviços de Segurança Privada'
        }
    
        df['TIPO_DESPESA'] = df['TIPO_DESPESA'].apply(lambda x: corrections.get(x, x))

    # Call the function to correct the 'TIPO_DESPESA' column
    correct_tipo_despesa(df)

    #To drop all lines that have NaN values in the 'COD_DOCUMENTO' column
    df.dropna(subset=['COD_DOCUMENTO'], inplace=True)

    #Creating CSV aggregated
    df_2 = df.groupby(['Month-Year', 'SENADOR'])['VALOR_REEMBOLSADO'].sum().reset_index()
    df_2['Contagem_Mes'] = df_2.groupby('SENADOR')['Month-Year'].rank(method='dense').astype(int)
    df_2['VALOR_REEMBOLSADO'] = df_2['VALOR_REEMBOLSADO'].astype(str).str.replace(',', '.')
    df_2['VALOR_REEMBOLSADO'] = df_2['VALOR_REEMBOLSADO'].astype(float)
    

    #Create CSV
    df.to_csv('/home/orlando_linux/alura_challange/csv_gold/csv_info_clean.csv', index=False, encoding='utf-8')
    df_2.to_csv('/home/orlando_linux/alura_challange/csv_gold/csv_info_clean_agg.csv', index=False, encoding='utf-8')

if __name__ == "__main__":
    generate_csv()
