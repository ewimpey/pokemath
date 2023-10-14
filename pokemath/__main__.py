import sys
from PyQt5.QtWidgets import QApplication
from pokemath.gui import PokemonChooser
#from src.pokemon_data import all_pokemon  
from pokemath.data_loader import load_data

def main():
    app = QApplication(sys.argv)

    # Load Pokemon and Move data
    #all_pokemon = [squirtle, charmander, bulbasaur]
    all_pokemon, all_moves = load_data()
    
    window = PokemonChooser(all_pokemon)
    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
