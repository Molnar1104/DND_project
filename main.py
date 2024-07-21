# main.py
import fitz
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QDialog, QFormLayout, QLabel, QLineEdit, QComboBox
import sqlite3
from dnd_classes import get_class_instance

def fill_pdf(character, input_pdf, output_pdf):
    doc = fitz.open(input_pdf)
    for page in doc:
        for field in page.widgets():
            field_name = field.field_name
            if field_name in character:
                field.set_text(character[field_name])
    doc.save(output_pdf)


# Database setup functions
def create_connection():
    return sqlite3.connect('dnd_characters.db')

def get_schema_version(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='schema_version';")
    if cursor.fetchone():
        cursor.execute("SELECT version FROM schema_version;")
        return cursor.fetchone()[0]
    return 0

def set_schema_version(cursor, version):
    cursor.execute("INSERT OR REPLACE INTO schema_version (version) VALUES (?)", (version,))

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    
    # Create schema_version table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS schema_version (
        version INTEGER PRIMARY KEY
    )
    ''')
    cursor.execute("INSERT OR REPLACE INTO schema_version (version) VALUES (0);")

    # Get current schema version
    schema_version = get_schema_version(cursor)

    # Apply schema updates
    if schema_version < 1:
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS characters (
            id INTEGER PRIMARY KEY,
            name TEXT,
            race TEXT,
            class TEXT,
            level INTEGER,
            strength INTEGER,
            dexterity INTEGER,
            constitution INTEGER,
            intelligence INTEGER,
            wisdom INTEGER,
            charisma INTEGER,
            hit_points INTEGER,
            equipment TEXT,
            proficiencies TEXT
        )
        ''')
        set_schema_version(cursor, 1)
    
    # Add more schema changes here if needed, incrementing the version number

    conn.commit()
    conn.close()

def insert_character(character):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO characters (name, race, class, level, strength, dexterity, constitution, intelligence, wisdom, charisma, hit_points, equipment, proficiencies)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (character['name'], character['race'], character['class'], character['level'],
          character['strength'], character['dexterity'], character['constitution'],
          character['intelligence'], character['wisdom'], character['charisma'],
          character['hit_points'], character['equipment'], character['proficiencies']))
    conn.commit()
    conn.close()

# Call to create the table if it doesn't exist
create_table()

class CharacterCreationForm(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Create New Character')
        self.setGeometry(100, 100, 400, 600)

        layout = QFormLayout()

        self.name_input = QLineEdit()
        self.race_input = QComboBox()
        self.class_input = QComboBox()
        self.level_input = QLineEdit()

        self.strength_input = QLineEdit()
        self.dexterity_input = QLineEdit()
        self.constitution_input = QLineEdit()
        self.intelligence_input = QLineEdit()
        self.wisdom_input = QLineEdit()
        self.charisma_input = QLineEdit()

        # Add races and classes as examples
        self.race_input.addItems(['Human', 'Elf', 'Dwarf', 'Halfling'])
        self.class_input.addItems(['Barbarian', 'Fighter', 'Wizard', 'Rogue', 'Cleric'])

        layout.addRow('Name:', self.name_input)
        layout.addRow('Race:', self.race_input)
        layout.addRow('Class:', self.class_input)
        layout.addRow('Level:', self.level_input)

        layout.addRow('Strength:', self.strength_input)
        layout.addRow('Dexterity:', self.dexterity_input)
        layout.addRow('Constitution:', self.constitution_input)
        layout.addRow('Intelligence:', self.intelligence_input)
        layout.addRow('Wisdom:', self.wisdom_input)
        layout.addRow('Charisma:', self.charisma_input)

        self.save_btn = QPushButton('Save Character')
        self.save_btn.clicked.connect(self.save_character)

        layout.addWidget(self.save_btn)

        self.setLayout(layout)

    def save_character(self):
        character_class = get_class_instance(self.class_input.currentText())
        level = int(self.level_input.text())
        constitution = int(self.constitution_input.text())
        
        character = {
            'name': self.name_input.text(),
            'race': self.race_input.currentText(),
            'class': self.class_input.currentText(),
            'level': level,
            'strength': int(self.strength_input.text()),
            'dexterity': int(self.dexterity_input.text()),
            'constitution': constitution,
            'intelligence': int(self.intelligence_input.text()),
            'wisdom': int(self.wisdom_input.text()),
            'charisma': int(self.charisma_input.text()),
            'hit_points': character_class.calculate_hit_points(level, constitution),
            'equipment': str(character_class.equipment),
            'proficiencies': str(character_class.proficiencies.get_proficiencies())
        }
        insert_character(character)
        fill_pdf(character, 'Blank D&D Character Sheet.pdf', 'Filled_Character_Sheet.pdf')

        print(f'Saving character: {character}')
        self.accept()  # Close the form after saving

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('D&D Character Builder')
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.new_character_btn = QPushButton('Create New Character')
        self.new_character_btn.clicked.connect(self.open_character_creation)

        self.view_characters_btn = QPushButton('View Existing Characters')
        self.view_characters_btn.clicked.connect(self.view_characters)

        layout.addWidget(self.new_character_btn)
        layout.addWidget(self.view_characters_btn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def open_character_creation(self):
        self.character_creation_form = CharacterCreationForm()
        self.character_creation_form.exec_()

    def view_characters(self):
        # Placeholder for viewing existing characters
        print('Existing characters will be displayed.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Apply the stylesheet to the entire application
    app.setStyleSheet("""
        QWidget {
            font-size: 14px;
            font-family: Arial, Helvetica, sans-serif;
            background-color: #f0f0f0;
        }
        QMainWindow {
            background-color: #ffffff;
        }
        QPushButton {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            transition-duration: 0.4s;
            cursor: pointer;
            border-radius: 5px;
        }
        QPushButton:hover {
            background-color: white;
            color: black;
            border: 2px solid #4CAF50;
        }
        QLineEdit {
            padding: 5px;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        QComboBox {
            padding: 5px;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        QLabel {
            font-weight: bold;
        }
    """)

    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
