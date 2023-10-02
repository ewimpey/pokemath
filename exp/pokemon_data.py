from .pokemon import Pokemon
from .move import Move

# Define Moves
tackle = Move("Tackle", 10, None, "Rock")
water_gun = Move("Water Gun", 15, "Fire", "Grass")
scratch = Move("Scratch", 12, None, "Rock")
vine_whip = Move("Vine Whip", 15, "Water", "Fire")
ember = Move("Ember", 15, "Grass", "Water")

# Define Pokemon
squirtle = Pokemon("Squirtle", 50, "Water", "img\\squirtle.png", [tackle, water_gun])
charmander = Pokemon("Charmander", 50, "Fire", "img\\charmander.png", [scratch, ember])
bulbasaur = Pokemon("Bulbasaur", 50, "Grass", "img\\bulbasaur.png", [tackle, vine_whip])

all_pokemon = [squirtle, charmander, bulbasaur]
