import data_explorer

df = data_explorer.get_import("FRA", "2020", "2021")

print(df.head())
