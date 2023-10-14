import random
import pkg_resources

# Defining the Pokemon class
class Pokemon:
    def __init__(self, name, health, type_, image_path, possible_moves):
        self.name = name
        self.health = health
        self.original_health = health
        self.type_ = type_
        adjusted_image_path = '../' + image_path 
        self.image_path = pkg_resources.resource_filename('pokemath', adjusted_image_path)
        #self.image_path = pkg_resources.resource_filename('pokemath', image_path)
        self.possible_moves = possible_moves
        self.equipped_moves = []
        
    def attack(self, opponent, bonus=0, move=None):
        effectiveness = ""
        # Use move's type and effectiveness
        if not move:
            move_power = 10
        else:
            move_power = move.power
            if any(t.lower() in map(str.lower, opponent.type_) for t in move.strength_against):
                effectiveness = "It's super effective!"
                move_power *= 1.5
                print("Move super effective, power amplified")
            elif any(t.lower() in map(str.lower, opponent.type_) for t in move.weakness_against):
                effectiveness = "It's not very effective..."
                move_power *= 0.5
                print("Move not effective, power diminished")
        total_damage = max(round(move_power + bonus + random.randint(-5, 5)), 1)
        opponent.health -= total_damage
        return total_damage, effectiveness

    def display_image(self):
        display(Image(filename=self.image_path, height=300, width=300))
        
    def equip_moves(self, n=3):
        n_moves = min(n, len(self.possible_moves))  # Use min to avoid sampling more moves than available
        self.equipped_moves = random.sample(self.possible_moves, n_moves) 

