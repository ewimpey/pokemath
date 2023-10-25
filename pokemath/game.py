import random
from .pokemon import Pokemon
from .move import Move
from .question_generator import generate_math_question

class Game:
    def __init__(self):
        self.player_pokemon = None
        self.opponent_pokemon = None
        self.attack_bonus = 0
    
    def initialize_game(self, player_pokemon_choice, all_pokemon):
        self.assign_player_pokemon(player_pokemon_choice, all_pokemon)
        self.assign_opponent_pokemon(all_pokemon)
        self.opponent_pokemon.equip_moves(2)
 
    def assign_player_pokemon(self, player_pokemon_choice, all_pokemon):
        self.player_pokemon = [poke for poke in all_pokemon if poke.image_path == player_pokemon_choice][0]

    def assign_opponent_pokemon(self, all_pokemon, hp_range=20):
        all_pokemon = [poke for poke in all_pokemon if poke != self.player_pokemon]  # Exclude the player's Pokémon
        possible_opponents = [
            poke for poke in all_pokemon 
            if self.player_pokemon.original_health - hp_range <= poke.original_health <= self.player_pokemon.original_health + hp_range
        ]
        
        # If there are possible opponents within the HP range, choose one randomly
        if possible_opponents:
            self.opponent_pokemon = random.choice(possible_opponents)
        else:
            # If no Pokémon within the HP range, choose any random Pokémon
            self.opponent_pokemon = random.choice(all_pokemon)

    def execute_move(self, selected_move_name, selected_categories):
        selected_move = None
        for move in self.player_pokemon.equipped_moves:
            if move.name == selected_move_name:
                selected_move = move
                break

        if selected_move:
            damage, effectiveness = self.player_pokemon.attack(self.opponent_pokemon, self.attack_bonus, selected_move)

        # Generate the math question
        question, answer = generate_math_question(self.player_pokemon, self.opponent_pokemon, damage, selected_categories)

        return damage, effectiveness, question, answer
