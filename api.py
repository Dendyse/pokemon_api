import requests
def get_pokemon(name):
    data = requests.get(f'https://pokeapi.co/api/v2/pokemon/{name}').json()
    type1 = data['types'][0]['type']['name']
    if len(data['types']) == 2:
        type2 = data['types'][1]['type']['name']
    else:
        type2 = None
    stat = {}
    for s in data['stats']:
        stat[s['stat']['name']] = s['base_stat']
    stat['id'] = data['id']
    stat['name'] = data['name']
    stat['type1'] = type1
    stat['type2'] = type2
    data2 = requests.get(f'https://pokeapi.co/api/v2/pokemon-species/{name}').json()
    if data2['evolves_from_species'] is None:
        stat['evolution'] = False
    else:
        stat['evolution'] = True
    return stat
