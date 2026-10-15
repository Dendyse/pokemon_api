from dotenv import load_dotenv
import os
from fastapi import FastAPI, HTTPException
import psycopg
from psycopg.rows import dict_row
from pydantic import BaseModel
app = FastAPI()
load_dotenv()
connection = psycopg.connect(
    dbname = 'Pokemon',
    user = 'postgres',
    password = os.getenv('DB_PASSWORD'),
    host = 'localhost',
    port = 5432
)
class Pokemon(BaseModel):
     id: int
     name: str
     type: str
     type_extra: str|None = None
     evolution: bool
     hp: int
     attack: int
     deff: int
     special_attack: int
     special_deff: int
     speed: int


cur = connection.cursor(row_factory=dict_row)
@app.get('/pokemon/{name}')
def pokemon_gen(name: str):
    cur.execute('SELECT * FROM Pokemon WHERE name = %s', (name,))
    row = cur.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Покемон не найден")
    else:
        return row

@app.get('/pokemon/type/{type}')
def pokemon_type(type: str):
    cur.execute('SELECT * FROM Pokemon WHERE type = %s OR type_extra = %s ORDER BY id', (type, type,))
    rows = cur.fetchall()
    if not rows:
        raise HTTPException(status_code=404, detail='Такого типа не существует')
    return rows

@app.get('/pokemon/top/{stat}')
def pokemon_top(stat: str):
    allowed = ['hp','attack', 'deff', 'special_attack', 'special_deff', 'speed']
    if stat not in allowed:
            raise HTTPException(status_code=400, detail=f'Такого стата как {stat} не существует')
    cur.execute(f'SELECT * FROM Pokemon ORDER BY {stat} DESC LIMIT 10')
    rows = cur.fetchall()
    return rows

@app.post('/pokemon')
def new_pokemon(pokemon: Pokemon):
    try:
        cur.execute ('INSERT INTO Pokemon (id, name, type, type_extra, evolution, hp, attack, deff, special_attack, special_deff, speed) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (pokemon.id, pokemon.name, pokemon.type, pokemon.type_extra, pokemon.evolution, pokemon.hp, pokemon.attack, pokemon.deff, pokemon.special_attack, pokemon.special_deff, pokemon.speed))
        connection.commit()
    except psycopg.errors.UniqueViolation:
         connection.rollback()
         raise HTTPException(status_code= 409, detail='Запрос не может быть выполнен так как такой id уже существует')
    return pokemon

@app.put('/pokemon/{name}')
def change_pokemon(name: str, pokemon: Pokemon):
     cur.execute('UPDATE Pokemon SET type = %s, type_extra = %s, evolution = %s, hp = %s, attack = %s, deff = %s, special_attack = %s, \
     special_deff = %s, speed = %s, name = %s WHERE name = %s', (pokemon.type, pokemon.type_extra, pokemon.evolution, 
                                                                pokemon.hp, pokemon.attack, pokemon.deff, pokemon.special_attack, 
                                                                pokemon.special_deff, pokemon.speed, pokemon.name, name))
     if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail= 'Покемон не найлен')
     else:
        connection.commit()
        return pokemon 
     
@app.delete('/pokemon/{name}')
def delete_pokemon(name: str):
    cur.execute('DELETE from Pokemon WHERE name = %s', (name,))
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail= 'Покемон не найден')
    connection.commit()
    return name