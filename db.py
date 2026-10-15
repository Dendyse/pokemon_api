from api import get_pokemon
import psycopg
import os
from dotenv import load_dotenv
load_dotenv()
connection = psycopg.connect(
    dbname = 'Pokemon',
    user = 'postgres',
    password = os.getenv('DB_PASSWORD'),
    host = 'localhost',
    port = 5432
)
def load_pokemon():
    cur = connection.cursor()
    for i in range (1, 152, 1):
        pok = get_pokemon(i)
        cur.execute (
            'INSERT INTO Pokemon(id, name, type, type_extra, evolution, hp, attack, deff, special_attack, special_deff, speed) '
            'VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s)', (pok['id'], pok['name'], pok['type1'], pok['type2'], pok['evolution'], pok['hp'],
            pok['attack'], pok['defense'], pok['special-attack'], pok['special-defense'], pok['speed'])
            )                                                    
    connection.commit()
    connection.close()

if __name__ == '__main__':
    load_pokemon()