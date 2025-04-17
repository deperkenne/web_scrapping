import pandas as pd
df = pd.read_csv('sport & Freizeit.csv')
df.to_excel('Sport&Freizeit.xlsx', index=False)
