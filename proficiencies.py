# proficiencies.py

class Proficiency:
    def __init__(self, type_, items):
        self.type = type_
        self.items = items

class Proficiencies:
    def __init__(self):
        self.proficiencies = {}

    def add_proficiency(self, source, proficiency):
        if source not in self.proficiencies:
            self.proficiencies[source] = []
        self.proficiencies[source].append(proficiency)

    def get_proficiencies(self):
        all_proficiencies = {}
        for source, profs in self.proficiencies.items():
            for proficiency in profs:
                if proficiency.type not in all_proficiencies:
                    all_proficiencies[proficiency.type] = set()
                all_proficiencies[proficiency.type].update(proficiency.items)
        return all_proficiencies
