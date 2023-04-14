import sys

from views import view_main
from controllers import create_menus
from controllers import player_controller
from controllers import tournament_controller
from models import player_model


class HomeMenuController:
    """Display the title and leads to the main menu"""

    def __init__(self):
        self.view = view_main.MainDisplay()
        self.clear = view_main.ClearScreen()
        self.create_menu = create_menus.CreateMenus()
        self.choosen_controller = None

    def __call__(self):
        self.clear()
        self.view.display_title()
        entry = self.create_menu(self.create_menu.main_menu)

        if entry == "1":
            self.choosen_controller = PlayerMenuController()
        elif entry == "2":
            self.choosen_controller = TournamentMenuController()
        elif entry == "3":
            self.choosen_controller = QuitAppController()

        return self.choosen_controller()


class PlayerMenuController(HomeMenuController):
    """Display the player menu and leads to the different options"""

    def __init__(self):
        super().__init__()
        self.create_player = player_controller.CreatePlayerController()
        self.players_report = player_controller.PlayerReport()
        self.home_menu_controller = HomeMenuController()
        self.player_model = player_model.Player()

    def __call__(self):
        while True:
            entry = self.create_menu(self.create_menu.player_menu)
            if entry == "1":
                self._create_player()
            elif entry == "2":
                self._update_ranking()
            elif entry == "3":
                self._display_players_report()
            elif entry == "4":
                self.home_menu_controller()
                break
            else:
                print("Entrée invalide. Veuillez entrer un chiffre correspondant à une option.")

    def _create_player(self):
        self.create_player()

    def _update_ranking(self):
        self.player_model.update_ranking()

    def _display_players_report(self):
        self.players_report()


class TournamentMenuController(HomeMenuController):
    """Display the tournament menu and leads to the different options"""
    def __init__(self):
        super().__init__()
        self.tournament_report_controller = tournament_controller.TournamentReport()
        self.create_tournament = tournament_controller.CreateTournamentController()
        self.home_menu_controller = HomeMenuController()
        self.start_tournament = tournament_controller.StartTournament()

    def __call__(self):
        entry = self.create_menu(self.create_menu.tournament_menu)
        if entry == "1":
            self.choosen_controller = self.create_tournament()
        if entry == "2":
            self.choosen_controller = self.start_tournament()
        if entry == "3":
            self.choosen_controller = self.start_tournament.load_tournament_statement()
        if entry == "4":
            self.choosen_controller = self.tournament_report_controller()
        if entry == "5":
            self.choosen_controller = self.home_menu_controller()


class QuitAppController:

    def __call__(self):
        sys.exit()
