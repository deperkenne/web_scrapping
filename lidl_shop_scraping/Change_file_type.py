import pandas as pd
df = pd.read_csv('DataFiles/Sport & Freizeit.csv')
df.to_excel('Sport&Freizeit.xlsx', index=False)
