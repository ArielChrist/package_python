import requests
import pandas as pd
import json

def get_worldbank_data(pays: str, date_debut: str, date_fin: str, indicateur: str) -> pd.DataFrame:
    url = f"https://api.worldbank.org/v2/country/{pays}/indicator/{indicateur}"
    params = {
        "format": "json",
        "date": f"{date_debut}:{date_fin}",
        "per_page": 1000 
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    data = json.loads(response.content)
    
    df = pd.DataFrame(data[1])
    
    if not df.empty:
        df['value'] = df['value'].apply(lambda x: x if pd.isna(x) else float(x))
        
        df['country_name'] = df['country'].apply(lambda x: x['value'] if isinstance(x, dict) else None)
        df['country_code'] = df['country'].apply(lambda x: x['id'] if isinstance(x, dict) else None)
        
        df['indicator_name'] = df['indicator'].apply(lambda x: x['value'] if isinstance(x, dict) else None)
        df['indicator_code'] = df['indicator'].apply(lambda x: x['id'] if isinstance(x, dict) else None)
        
        df = df.drop(['country', 'indicator'], axis=1)
    return df

def get_import(pays: str, date_debut: str, date_fin: str, indicateur = "NE.IMP.GNFS.CD") -> pd.DataFrame:
    return get_worldbank_data(pays, date_debut, date_fin, indicateur)

def get_export(pays: str, date_debut: str, date_fin: str, indicateur = "NE.EXP.GNFS.CD") -> pd.DataFrame:
    return get_worldbank_data(pays, date_debut, date_fin, indicateur)

def get_pib(pays: str, date_debut: str, date_fin: str, indicateur = "NY.GDP.MKTP.CD") -> pd.DataFrame:
    return get_worldbank_data(pays, date_debut, date_fin, indicateur)

def main():
    print("Données des importations pour la Centrafrique de 2021 à 2024 :")
    imports = get_import("CF", "2021", "2024")
    print(imports.head())

    print("\nDonnées des exportations du Sénégal de 2020 à 2025 :")
    exports = get_export("SN", "2020", "2025")
    print(exports.head())

    print("\nDonnées du PIB du Sénégal de 2020 à 2025 :")
    pib = get_pib("SN", "2020", "2025")
    print(pib.head())

if __name__ == "__main__":
    main()