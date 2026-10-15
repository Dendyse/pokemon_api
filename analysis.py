import pandas as pd
import os
from dotenv import load_dotenv
import psycopg
import matplotlib.pyplot as plt
load_dotenv()
connection = psycopg.connect(
    dbname = 'Pokemon',
    user = 'postgres',
    password = os.getenv('DB_PASSWORD'),
    host = 'localhost',
    port = 5432
)
df = pd.read_sql('SELECT * FROM Pokemon', connection)
df_new = df.groupby('evolution')[['speed', 'hp', 'attack', 'deff','special_attack', 'special_deff']].mean()
dif = (((df_new.loc[True] - df_new.loc[False]) / df_new.loc[False])*100)
print(dif.sort_values())

dif.sort_values().plot(kind = 'barh')
plt.title('Рост стат. после эволюции покемона в среднем, в %')
plt.xlabel('Процент')
plt.tight_layout()
plt.show()