# Defining the Move class
class Move:
    def __init__(self, name, power, strength_against=None, weakness_against=None):
        self.name = name
        self.power = power
        self.strength_against = strength_against if strength_against is not None else []
        self.weakness_against = weakness_against if weakness_against is not None else []

    def is_strong_against(self, other_type):
        return other_type in self.strength_against

    def is_weak_against(self, other_type):
        return other_type in self.weakness_against
