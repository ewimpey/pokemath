import json
from .pokemon import Pokemon
from .move import Move

def load_data():
    # Load the moves data from the JSON file
    with open('src\\moves_data.json', 'r') as file:
        moves_data = json.load(file)

    # Create Move objects from the loaded data, return empty list if no strength or weakness
    all_moves = {data['name']: Move(data['name'], data['power'], data.get('strength_against', []), data.get('weakness_against', [])) for data in moves_data}

    # Load the Pokémon data from the JSON file
    with open('src\\pokemon_data.json', 'r') as file:
        pokemon_data = json.load(file)

    # Create Pokémon objects from the loaded data
    all_pokemon = []
    for data in pokemon_data:
        moves = [all_moves[name] for name in data['moves'] if name in all_moves]
        if moves:
            pokemon = Pokemon(data['name'], data['health'], data['types'], data['image_path'], moves)
            all_pokemon.append(pokemon)

    return all_pokemon, all_moves
