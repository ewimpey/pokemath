from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QListView, QLineEdit,
    QLabel, QProgressBar, QPushButton, QCheckBox, QMessageBox, QInputDialog
)
from PyQt5.QtGui import QPixmap, QStandardItemModel, QStandardItem
from PyQt5.QtCore import QSortFilterProxyModel, Qt
#from PyQt5 import QtCore

from .game import Game
import random

class PokemonChooser(QMainWindow):
    def __init__(self, all_pokemon):
        super().__init__()
        self.game = Game()
        self.all_pokemon = all_pokemon
        self.pokemon_buttons = []
        
        # Set window properties
        self.setWindowTitle("Choose Your Pokémon")
        self.setGeometry(100, 100, 1200, 800)

        # Create a widget to hold content
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Set main layout for central_widget
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Pokémon layout (horizontal layout)
        pokemon_layout = QHBoxLayout()

        # Player's Pokémon and health bar (vertical layout)
        v_player_layout = QVBoxLayout()
        self.lbl_player_image = QLabel(self)
        v_player_layout.addWidget(self.lbl_player_image)
        self.player_health_bar = QProgressBar(self)
        v_player_layout.addWidget(self.player_health_bar)
        pokemon_layout.addLayout(v_player_layout)

        # Opponent's Pokémon and health bar (vertical layout)
        v_opponent_layout = QVBoxLayout()
        self.lbl_opponent_image = QLabel(self)
        v_opponent_layout.addWidget(self.lbl_opponent_image)
        self.opponent_health_bar = QProgressBar(self)
        v_opponent_layout.addWidget(self.opponent_health_bar)
        pokemon_layout.addLayout(v_opponent_layout)

        main_layout.addLayout(pokemon_layout)

        self.pokemon_list_view = QListView(self)  # Create a QListView widget
        pokemon_model = QStandardItemModel(self.pokemon_list_view)  # Create a model for the list view

        for pokemon in self.all_pokemon:
            item = QStandardItem(pokemon.name)  # Create an item with Pokémon name
            pokemon_model.appendRow(item)  # Add the item to the model

        self.pokemon_list_view.setModel(pokemon_model)  # Set the model for the list view
        main_layout.addWidget(self.pokemon_list_view)  # Add the list view to the layout

        self.pokemon_list_view.clicked.connect(self.pokemon_selected)

        # Search capability for selecting pokemon
        self.search_box = QLineEdit(self)
        main_layout.addWidget(self.search_box)

        self.proxy_model = QSortFilterProxyModel(self)
        self.proxy_model.setSourceModel(pokemon_model)
        self.proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.pokemon_list_view.setModel(self.proxy_model)
        self.search_box.textChanged.connect(self.on_search_box_text_changed)

        # Check boxes for math categories
        checkbox_layout = QVBoxLayout()

        # Setting up individual checkboxes
        add_sub_checkbox = QCheckBox("Addition/Subtraction")
        mul_div_checkbox = QCheckBox("Multiplication/Division")
        carson_checkbox = QCheckBox("Carson")

        # Add the checkboxes to the checkbox layout
        checkbox_layout.addWidget(add_sub_checkbox)
        checkbox_layout.addWidget(mul_div_checkbox)
        checkbox_layout.addWidget(carson_checkbox)

        # Add the checkbox layout to the main layout
        main_layout.addLayout(checkbox_layout)

        # Move buttons for Pokémon
        self.move_buttons = []
        for _ in range(3):  # Initialize two move buttons
            btn_move = QPushButton("", self)
            btn_move.hide()  # Initially hidden
            btn_move.clicked.connect(self.execute_move)
            self.move_buttons.append(btn_move)
            main_layout.addWidget(btn_move) 
        
        # Creating math_category attribute
        self.math_categories = {
            "add_sub": add_sub_checkbox,
            "mul_div": mul_div_checkbox,
            "Carson": carson_checkbox
        }

    def on_search_box_text_changed(self, text):
        self.proxy_model.setFilterRegExp(text)

    def pokemon_selected(self, index):
        selected_pokemon_name = index.data()
        selected_pokemon = next(p for p in self.all_pokemon if p.name == selected_pokemon_name)
        self.initialize_game(selected_pokemon.image_path)
        self.pokemon_list_view.hide()
        self.search_box.hide()

    def connect_button(self, button, pokemon):
        button.clicked.connect(lambda: self.initialize_game(pokemon.image_path))

    def initialize_game(self, player_pokemon_choice):

        #for debugging:
        print(f"Player Pokemon Choice: {player_pokemon_choice}")
        
        # code to keep...

        self.game.initialize_game(player_pokemon_choice, self.all_pokemon)
        self.display_image(self.lbl_player_image, self.game.player_pokemon.image_path)
        self.display_image(self.lbl_opponent_image, self.game.opponent_pokemon.image_path)

        self.player_health_bar.setMaximum(self.game.player_pokemon.original_health)
        self.player_health_bar.setValue(self.game.player_pokemon.health)
        self.player_health_bar.setFormat("%v")
        self.opponent_health_bar.setMaximum(self.game.opponent_pokemon.original_health)
        self.opponent_health_bar.setValue(self.game.opponent_pokemon.health)
        self.opponent_health_bar.setFormat("%v")
        
        self.display_moves()

        # dynamic, scalable, testing:
        for btn in self.pokemon_buttons:
            btn.hide()

    def execute_move(self):
        sender = self.sender()
        selected_move_name = sender.text()
        selected_categories = self.get_selected_categories()

            # Check if any category is selected
        if not selected_categories:
            QMessageBox.warning(self, "No Category Selected", "Please select at least one math category before choosing a move.")
            return

        damage, effectiveness, question, answer = self.game.execute_move(selected_move_name, selected_categories)

        QMessageBox.information(self, "Attack", f"{self.game.player_pokemon.name} used {selected_move_name} and dealt {damage} damage! {effectiveness}")
        
        if self.game.opponent_pokemon.health <= 0:
            self.opponent_health_bar.setValue(self.game.opponent_pokemon.health)
            QMessageBox.information(self, "Victory", f"{self.game.opponent_pokemon.name} is defeated! You win!")
            self.reset_game()
        else:
            player_answer, ok = QInputDialog.getDouble(self, "Math Question", question)
            self.opponent_health_bar.setValue(self.game.opponent_pokemon.health)
            self.game.attack_bonus = 0

            if ok and abs(player_answer - answer) < 1:
                QMessageBox.information(self, "Correct!", "You answered correctly!")
                item, ok = QInputDialog.getItem(self, "Choose Your Bonus", "Select a bonus:", ["Attack Bonus (Extra 5 damage on next attack)", "Health Bonus (Regain 10 health points)"], 0, False)
                if ok and item:
                    if item == "Attack Bonus (Extra 5 damage on next attack)":
                        self.game.attack_bonus = 5
                    else:
                        self.game.player_pokemon.health += 10
                        if self.game.player_pokemon.health > 100:
                            self.game.player_pokemon.health = 100
                        self.player_health_bar.setValue(self.game.player_pokemon.health)
            else:
                QMessageBox.warning(self, "Wrong!", f"The correct answer was {answer:.2f}.")

            # Opponent's Turn
            opponent_move = random.choice(self.game.opponent_pokemon.equipped_moves)
            damage, effectiveness = self.game.opponent_pokemon.attack(self.game.player_pokemon, 0, opponent_move)
            QMessageBox.information(self, "Opponent's Attack", f"{self.game.opponent_pokemon.name} used {opponent_move.name} and dealt {damage} damage! {effectiveness}")
            self.player_health_bar.setValue(self.game.player_pokemon.health)

            if self.game.player_pokemon.health <= 0:
                QMessageBox.information(self, "Defeat", f"{self.game.player_pokemon.name} is defeated! You lose.")
                self.reset_game()
            elif self.game.opponent_pokemon.health <= 0:
                QMessageBox.information(self, "Victory", f"{self.game.opponent_pokemon.name} is defeated! You win!")
                self.reset_game()

    def display_image(self, label, image_path):
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaled(400, 400)
        label.setPixmap(pixmap)

    def get_selected_categories(self):
        return [cat for cat, checkbox in self.math_categories.items() if checkbox.isChecked()]

    def display_moves(self):
        self.game.player_pokemon.equip_moves(3)
        for i, move in enumerate(self.game.player_pokemon.equipped_moves):
            self.move_buttons[i].setText(move.name)
            self.move_buttons[i].show()

    def reset_game(self):
        self.game.player_pokemon.health = self.game.player_pokemon.original_health
        self.game.opponent_pokemon.health = self.game.opponent_pokemon.original_health
        self.lbl_player_image.clear()
        self.lbl_opponent_image.clear()
        self.player_health_bar.setValue(self.game.player_pokemon.original_health)
        self.opponent_health_bar.setValue(self.game.opponent_pokemon.original_health)
        for btn in self.move_buttons:
            btn.hide()
        
        self.pokemon_list_view.show()
        self.search_box.clear()
        self.search_box.show()

