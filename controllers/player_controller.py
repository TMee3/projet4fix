from operator import attrgetter

from controllers import main_control
from models import player_model
from views import view_main
from controllers import create_menus


class CreatePlayerController:
    """Enter all the player's details, then add the player in the database"""
    def __init__(self):
        self.player_values = []
        self.player_keys = ["Nom", "Prénom", "Date de naissance", "Sexe", "Classement"]
        self.home_menu_controller = main_control.HomeMenuController()

    def __call__(self):
        self.player_model = player_model.Player()
        self.player_values.append(self.add_last_name())
        self.player_values.append(self.add_first_name())
        self.player_values.append(self.add_birth_details())
        self.player_values.append(self.add_gender())
        self.player_values.append(self.add_ranking())
        if self.validate_player():
            self.player_model.add_to_database(self.player_values)
        self.player_values.clear()
        self.home_menu_controller()

    def add_last_name(self):
        valid_last_name = False
        while not valid_last_name:
            last_name = input("Entrez le nom de famille: ")
            if last_name != "":
                valid_last_name = True
            else:
                print("Vous devez entrer un nom")
        return last_name

    def add_first_name(self):
        valid_first_name = False
        while not valid_first_name:
            first_name = input("Entrez le prénom: ")
            if first_name != "":
                valid_first_name = True
            else:
                print("Vous devez entrer un prénom ")
        return first_name

    def add_birth_details(self):
        valid_birth_details = False
        while not valid_birth_details:
            birth_details = input("Entrez la date de naissance (jj/mm/aaaa): ")
            if len(birth_details) == 10 and birth_details[2] == "/" and birth_details[5] == "/":
                valid_birth_details = True
            else:
                print("Vous devez entrer une date de naissance valide (jj/mm/aaaa)")
        return birth_details

    def add_gender(self):
        valid_gender = False
        validated_gender = None
        while not valid_gender:
            gender = input("Choisissez le genre du joueur \n"
                           "'H' pour un homme \n'F' pour une femme: ")
            if gender == "H":
                valid_gender = True
                validated_gender = "Homme"
            elif gender == "F":
                valid_gender = True
                validated_gender = "Femme"
            else:
                print("Vous devez entrer un genre (H ou F)")
        return validated_gender

    def add_ranking(self):
        valid_ranking = False
        while not valid_ranking:
            ranking = input("Entrez le classement du joueur: ")
            if ranking.isdigit() and int(ranking) >= 0:
                valid_ranking = True
            else:
                print("Vous devez entrer un nombre entier positif")
        return int(ranking)

    def validate_player(self):
        view_main.FrameDisplay.display_datas_in_a_frame(self.player_values, self.player_keys)

        valid_player = False
        while not valid_player:
            validate_player = input("Valider le joueur ? (O/N): ")
            if validate_player == "O":
                valid_player = True
                return True
            elif validate_player == "N":
                valid_player = True
                return False
            else:
                print("Vous devez entrer O ou N")


class PlayerReport:
    """Display the players reports"""

    def __call__(self):
        self.create_menu = create_menus.CreateMenus()
        self.home_menu_controller = main_control.HomeMenuController()
        self.display_player = view_main.DisplayPlayersReport()
        self.players_database = player_model.player_database
        self.player = player_model.Player()
        player_serialized = []

        for player in self.players_database:
            player_serialized.append(self.player.unserialized(player))

        self.display_player()
        entry = self.create_menu(self.create_menu.players_report_menu)

        if entry == "1":
            player_serialized.sort(key=attrgetter("last_name"))
            self.display_player.display_alphabetical(player_serialized)
            PlayerReport.__call__(self)
        if entry == "2":
            player_serialized.sort(key=attrgetter("ranking"))
            self.display_player.display_ranking(player_serialized)
            PlayerReport.__call__(self)
        if entry == "3":
            self.home_menu_controller()
