import json

class NoteFingering:
    def __init__(self, holes):
        self.holes = holes

    def __repr__(self):
        return f"{self.holes}" 
    
    def is_empty(self):
        return all(hole == 0 for hole in self.holes)

class NoteVariations:
    def __init__(self, note):
        self.note = note
        self.fingerings = []

    def add_fingering(self, fingering):
        self.fingerings.append(fingering)

    def __repr__(self):
        return f"{self.note} Fingerings: {self.fingerings}"

class FingeringSystem:
    def __init__(self, name):
        self.name = name
        self.notes = []
    def update_name(self, new_name):
        self.name = new_name

    def add_note_fingering(self, note_fingering):
        self.notes.append(note_fingering)

    def find_note_fingering(self, note_name):
        for note_fing in self.notes:
            if note_fing.note == note_name:
                return note_fing
        return None

    def load_from_file(self, filepath):
        with open(filepath, 'r') as file:
            data = json.load(file)
            self.name = data['name']
            for note_group in data['position']:
                for note_info in note_group:
                    note_name = note_info['name']
                    note_fingering = self.find_note_fingering(note_name)
                    if not note_fingering:
                        note_fingering = NoteVariations(note_name)
                        self.add_note_fingering(note_fingering)
                    new_fingering = NoteFingering(note_info['holes'])
                    note_fingering.add_fingering(new_fingering)

    def save_to_file(self, filepath):
        export_data = {
            "name": self.name,
            "position": []
        }
        for note_var in self.notes:
            group = []
            for fingering in note_var.fingerings:
                group.append({"name": note_var.note, "holes": fingering.holes})
            export_data['position'].append(group)

        with open(filepath, 'w') as file:
            json.dump(export_data, file, indent=4)
    
    def find_fingering_collisions(self):
        fingerprint_map = {}
        for note_var in self.notes:
            for fingering in note_var.fingerings:
                if not fingering.is_empty():
                    # Create a hashable representation of the fingering
                    fingerprint = tuple(fingering.holes)
                    if fingerprint not in fingerprint_map:
                        fingerprint_map[fingerprint] = []
                    fingerprint_map[fingerprint].append(note_var.note)

        # Filter out entries with less than two notes sharing the same fingering
        collisions = {fp: notes for fp, notes in fingerprint_map.items() if len(notes) > 1}
        return collisions

    def __repr__(self):
        return f"Fingering System: {self.name}, Notes: {self.notes}"
