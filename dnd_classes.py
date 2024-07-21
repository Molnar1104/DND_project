# dnd_classes.py
from proficiencies import Proficiency, Proficiencies

class DnDClass:
    def __init__(self, name):
        self.name = name
        self.hit_dice = None
        self.hit_points_first_level = None
        self.hit_points_higher_levels = None
        self.proficiencies = Proficiencies()
        self.equipment = []

    def calculate_hit_points(self, level, constitution_modifier):
        if level == 1:
            return self.hit_points_first_level + constitution_modifier
        else:
            return self.hit_points_first_level + constitution_modifier + (level - 1) * (self.hit_dice + constitution_modifier)

class Barbarian(DnDClass):
    def __init__(self):
        super().__init__('Barbarian')
        self.hit_dice = 12
        self.hit_points_first_level = 12
        self.hit_points_higher_levels = lambda level, con_mod: (12 + con_mod) * level
        self.proficiencies.add_proficiency('class', Proficiency('Armor', ['Light armor', 'Medium armor', 'Shields']))
        self.proficiencies.add_proficiency('class', Proficiency('Weapons', ['Simple weapons', 'Martial weapons']))
        self.proficiencies.add_proficiency('class', Proficiency('Saving Throws', ['Strength', 'Constitution']))
        self.proficiencies.add_proficiency('class', Proficiency('Skills', ['Animal Handling', 'Athletics', 'Intimidation', 'Nature', 'Perception', 'Survival']))
        self.equipment = [
            ('a greataxe', 'any martial melee weapon'),
            ('two handaxes', 'any simple weapon'),
            'An explorer\'s pack and four javelins'
        ]

# Example function to get the correct class instance
def get_class_instance(class_name):
    classes = {
        'Barbarian': Barbarian,
        # Add other classes here
    }
    return classes[class_name]()
