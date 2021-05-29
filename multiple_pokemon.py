import matplotlib.pyplot as plt
import requests

#My current key for the API
api_key = 'c2eaa76b-c34c-4d3a-8f33-da95a230d9ea'

def graph_cards(name_of_pokemon, poke_dict):
    endpoint = f'https://api.pokemontcg.io/v2/cards?q=name:{name_of_pokemon}'
    data = (requests.get(endpoint, data={'X-api-key': api_key})).json() 
    count = data['count']
    if count > 0:
        poke_dict[name_of_pokemon] = [count]
    else:
        print(f'{name_of_pokemon} is not a valid Pokemon name.')
    
poke_dict = {}

def make_graph(poke_dict):
    name = []
    number = []
    items = poke_dict.items()
    for item in items:
        name.append(item[0]), number.append(item[1][0])
    plt.barh(name, number)
    plt.show()

while True:
    pokemon_name = input("Enter a Pokemon name, or 'quit' to exit: ")
    if pokemon_name == 'quit':
        break
    else:
        graph_cards(pokemon_name, poke_dict)

make_graph(poke_dict)