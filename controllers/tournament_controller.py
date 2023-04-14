import time
from operator import itemgetter
from operator import attrgetter

import pandas as pd

from controllers import main_control
from controllers import create_menus
from models import tournament_model
from models import player_model
from views import view_main


class CreateTournamentController:
    """Create a tournament with entering all the details, then save it in the database"""

    def __init__(self):
        self.create_menu = create_menus.CreateMenus()
        self.tournament_values = []
        self.players_in_tournament = []
        self.players_ids = []
        self.players_serialized = []
        self.player = player_model.Player()
        self.home_menu_controller = main_control.HomeMenuController()
        self.tournament = tournament_model.Tournament()

    def __call__(self):
        self.tournament_values.append(self.add_tournament_name())
        self.tournament_values.append(self.add_location())
        self.tournament_values.append(self.add_tournament_date())
        self.tournament_values.append(self.add_number_of_rounds())
        self.tournament_values.append(self.add_time_control())
        self.tournament_values.append(self.add_description())
        self.add_players_to_tournament()
        self.tournament_values.append(self.players_in_tournament)
        self.tournament.add_to_database(self.tournament_values)
        self.home_menu_controller()

    def add_tournament_name(self):
        valid_tournament_name = False
        while not valid_tournament_name:
            tournament_name = input("Entrez le nom du tournoi: ")
            if tournament_name != "":
                valid_tournament_name = True
            else:
                print("Vous devez entrer un nom")
        return tournament_name

    def add_location(self):
        valid_location = False
        while not valid_location:
            location = input("Entrez l'endroit où se déroule le tournoi: ")
            if location != "":
                valid_location = True
            else:
                print("Vous devez entrer un endroit")
        return location

    def add_tournament_date(self):
        valid_date = False
        while not valid_date:
            tournament_date = input("Entrez la date du tournoi (jj/mm/aaaa): ")
            if len(tournament_date) == 10 and tournament_date[2] == "/" and tournament_date[5] == "/":
                valid_date = True
            else:
                print("Vous devez entrer une date valide (jj/mm/aaaa)")
        return tournament_date

    def add_number_of_rounds(self):
        number_of_rounds = 4
        print("Le nombre de rounds est de 4 par défaut\n"
            "Souhaitez-vous changer ce nombre ?")

        while True:
            print("Entrer 'Y' pour changer, ou 'N' pour continuer")
            choice = input("--> ")
            if choice == "Y":
                number_of_rounds = input("Entrez le nombre de rounds :")
                if number_of_rounds.isdigit():
                    break
                else:
                    print("Vous devez entrer un nombre entier")
            elif choice == "N":
                break

        return number_of_rounds

    def add_time_control(self):
        print("Choisissez le contrôle du temps:")
        time_control = None
        entry = self.create_menu(self.create_menu.time_control_menu)
        if entry == "1":
            time_control = "Bullet"
        if entry == "2":
            time_control = "Blitz"
        if entry == "3":
            time_control = "Coup rapide"
        return time_control

    def add_description(self):
        description = input("Entrer une description au tournoi :\n"
                            "-->")
        return description

    def add_players_to_tournament(self):
        """Add the ids of the selected players in a list, en return the list"""
        view_main.ClearScreen()

        valid_add_player_choice = False
        while not valid_add_player_choice:
            add_player_choice = input("\nVoulez-vous ajouter des joueurs ?\n\n"
                                    "Appuyer sur 'Y' pour confirmer, ou 'N' pour poursuivre")
            if add_player_choice == "Y":
                valid_add_player_choice = True
            elif add_player_choice == "N":
                return
            else:
                print("Appuyez sur 'Y' ou 'N'")

        display_players_database = pd.read_json("models/players.json")
        print(display_players_database)
        print()
        print("Vous devez choisir un nombre de joueurs pair")
        print()
        print("Joueurs dans le tournoi : " + str(self.players_ids))
        print()
        print("Entrez les numéros des joueurs séparés par des virgules :")

        valid_ids = False
        while not valid_ids:
            id_choices = input("--> ").split(',')
            id_choices = [id_choice.strip() for id_choice in id_choices]
            try:
                id_choices = [int(id_choice) for id_choice in id_choices]

            except ValueError:
                print("Vous devez entrer des nombres entiers séparés par des virgules")
            else:
                if any(id_choice <= 0 or id_choice > len(player_model.player_database) for id_choice in id_choices):
                    print("Vous devez choisir des joueurs dans la liste")
                elif len(id_choices) % 2 != 0:
                    print("Vous devez choisir un nombre de joueurs pair")
                else:
                    valid_ids = True

        for id_choice in id_choices:
            if id_choice in self.players_ids:
                print(f"\nLe joueur {id_choice} a déjà été choisi pour ce tournoi\n")
                continue

            self.players_ids.append(id_choice)
            print(f"Le joueur {id_choice} a été ajouté au tournoi")

        print("Joueurs dans le tournoi : " + str(self.players_ids))

        self.players_serialized = [player_model.player_database.get(doc_id=id) for id in self.players_ids]
        self.players_serialized.sort(key=itemgetter("Classement"), reverse=True)
        self.players_ids = [player.doc_id for player in self.players_serialized]
        self.tournament_values.append(self.players_ids.copy())


class StartTournament:
    """Controller who start the tournament, stop when the tournament is ended"""

    MATCHS_PLAYED = []
    TOURS_PLAYED = []

    def __call__(self):
        self.sorted_players = []
        self.tournament_menu_controller = main_control.TournamentMenuController()
        self.tour = tournament_model.Tour()
        self.view_final_scores = view_main.EndTournamentDisplay()
        self.home_menu_controller = main_control.HomeMenuController()

        # Ask to choose a tournament and return an instance of tournament
        self.tournament_object = self.select_a_tournament()

        # copy in the list "sorted_players" the players by ranking
        self.sorted_players = self.sort_player_first_tour(self.tournament_object)
        # 1st tour, copy the instance in tournament
        self.tournament_object.list_of_tours.append(self.tour.run(self.sorted_players, self.tournament_object))
        self.save_tournament_statement(self.tournament_object)

        # all the others tours
        for tour in range(int(self.tournament_object.number_of_tours) - 1):
            self.sorted_players.clear()
            self.sorted_players = self.sort_players_by_score(self.tournament_object.list_of_tours[tour])
            self.tournament_object.list_of_tours.append(self.tour.run(self.sorted_players, self.tournament_object))
            self.save_tournament_statement(self.tournament_object)

        self.view_final_scores(self.tournament_object)
        self.home_menu_controller()

    def save_tournament_statement(self, tournament_object):
        self.home_menu_controller = main_control.HomeMenuController()
        db_tournament = tournament_model.tournament_database
        tours_table = db_tournament.table("tours")

        tour_object = tournament_object.list_of_tours[-1]
        tour_serialized = tour_object.serialized()
        tour_serialized['Matchs'] = tour_object.list_of_finished_matchs

        tour_id = tours_table.insert(tour_serialized)
        StartTournament.TOURS_PLAYED.append(tour_id)
        db_tournament.update({"Tours": StartTournament.TOURS_PLAYED}, doc_ids=[tournament_object.tournament_id])

        print("Voulez vous sauvegarder et quitter le tournoi en cours ? Y / N")
        valid_choice = False
        while not valid_choice:
            choice = input("-->")
            if choice == 'Y':
                valid_choice = True
                self.home_menu_controller()
            elif choice == 'N':
                valid_choice = True
            else:
                print("Vous devez entrer 'Y' ou 'N'")

    def load_tournament_statement(self):
        # choisir un tournoi et calculer le nombre de tours restant
        sorted_players = []
        self.tournament = tournament_model.Tournament()
        self_display_tournament = view_main.LoadTournamentDisplay()
        self.home_menu_controller = main_control.HomeMenuController()
        self.tour = tournament_model.Tour()
        self.view_final_scores = view_main.EndTournamentDisplay()
        db_tournament = tournament_model.tournament_database
        tours_table = db_tournament.table("tours")
        tours_instances = []

        if self_display_tournament():  # True if there is tournaments already started
            valid_entry = False
            while not valid_entry:
                print("Entrez le chiffre correspondant au tournoi")
                choice = input("--> ")
                try:
                    int(choice)
                    valid_entry = True
                except Exception:
                    print("Vous devez entrer le chiffre correspondant au tournoi")
            else:
                choosen_tournament = tournament_model.tournament_database.get(doc_id=int(choice))
                for tour in choosen_tournament["Tours"]:
                    tour_serialized = tours_table.get(doc_id=tour)
                    tour_object = self.tour.unserialized(tour_serialized)
                    tours_instances.append(tour_object)
                choosen_tournament["Tours"] = tours_instances
                tournament_object = self.tournament.unserialized(choosen_tournament)

        else:
            print("Pas de tournoi en cours, retour au menu principal")
            time.sleep(1)
            self.home_menu_controller()

        for tour in range(int(tournament_object.number_of_tours) - len(tournament_object.list_of_tours)):
            sorted_players.clear()
            sorted_players = self.sort_players_by_score(tournament_object.list_of_tours[tour])
            tournament_object.list_of_tours.append(self.tour.run(sorted_players, tournament_object))
            self.save_tournament_statement(tournament_object)

        self.view_final_scores(tournament_object)
        self.home_menu_controller()

    def select_a_tournament(self):
        self.tournament = tournament_model.Tournament()
        self.display_tournaments = view_main.TournamentDisplay()
        self.home_menu_controller = main_control.HomeMenuController()

        if self.display_tournaments():

            valid_entry = False
            while not valid_entry:
                print("Entrez le chiffre correspondant au tournoi")
                choice = input("--> ")
                try:
                    choice.isdigit() is False
                    int(choice) < len(tournament_model.tournament_database)
                    int(choice) <= 0
                except Exception:
                    print("Vous devez entrer le chiffre correspondant au tournoi")
                else:
                    choosen_tournament = tournament_model.tournament_database.get(doc_id=int(choice))
                    tournament_object = self.tournament.unserialized(choosen_tournament)
                    return tournament_object
        else:
            print("Pas de tournois créé, veuillez créer un tournoi")
            time.sleep(1)
            self.home_menu_controller()

    def sort_player_first_tour(self, tournament):
        """ retourne une liste de joueurs triée par classement """
        self.player = player_model.Player()
        players_instances = [self.player.unserialized(player_model.player_database.get(doc_id=id)) for id in tournament.players_ids]
        sorted_players = []

        for i, player in enumerate(players_instances):
            if i + len(tournament.players_ids) // 2 < len(tournament.players_ids):
                opponent_index = i + len(tournament.players_ids) // 2
                opponent = players_instances[opponent_index]
                sorted_players[i*2:i*2+2] = [player, opponent]
                self.MATCHS_PLAYED.append({player.player_id, opponent.player_id})

        return sorted_players

    def sort_players_by_score(self, tour_instance):
        """ retourne une liste de joueurs triée par score """
        self.player = player_model.Player()
        players = [player for match in tour_instance.list_of_finished_matchs for player in match]
        players_sorted_by_score = []
        players_sorted_flat = []
        players_instance = []
        matches_played = [tuple(match) for match in self.MATCHS_PLAYED]
        match_to_try = set()

        players_sorted_by_score = players[:]

        for player in players_sorted_by_score:
            players_sorted_flat.append(player[0])

        players_sorted_by_score.clear()

        for player_id in players_sorted_flat:
            player = player_model.player_database.get(doc_id=player_id)
            players_instance.append(self.player.unserialized(player))

        # Tri des joueurs par score, et par classement si les scores sont égaux
        players_instance.sort(key=lambda player: (player.tournament_score, player.ranking), reverse=True)

        for i in range(0, len(players_instance), 2):
            player_1, player_2 = players_instance[i], players_instance[i+1]
            match_to_try.add(player_1.player_id)
            match_to_try.add(player_2.player_id)
            if tuple(match_to_try) in matches_played:
                print(f"Le match {player_1} CONTRE {player_2} a déjà eu lieu")
                time.sleep(1)
                match_to_try.discard(player_2.player_id)
                continue
            else:
                print(f"Ajout du match {player_1} CONTRE {player_2}")
                players_sorted_by_score.extend([player_1, player_2])
                matches_played.append(tuple(match_to_try))
                match_to_try.clear()
                time.sleep(1)

        return players_sorted_by_score


class TournamentReport:
    """Display the tournament reports"""

    def __call__(self):
        self.clear = view_main.ClearScreen()
        self.create_menu = create_menus.CreateMenus()
        self.display_tournament = view_main.DisplayTournamentsReport()
        self.display_player = view_main.DisplayPlayersReport()
        self.home_menu_controller = main_control.HomeMenuController()

        self.players_database = player_model.player_database
        self.player = player_model.Player()
        player_serialized = []
        self.tournament_database = tournament_model.tournament_database
        self.tournament = tournament_model.Tournament()
        tour_table = self.tournament_database.table("tours")
        tournament_serialized = []
        tournament_objects = []

        for tournament in self.tournament_database:
            tournament_objects.append(tournament)
            tournament_serialized.append(self.tournament.unserialized(tournament))

        self.clear()
        self.display_tournament()
        entry = self.create_menu(self.create_menu.tournaments_report_menu)

        # Display all the tournaments
        if entry == "1":
            for tournament in tournament_serialized:
                for id in tournament.players_ids:
                    player = self.players_database.get(doc_id=id)
                    player_serialized.append(self.player.unserialized(player))
            self.display_tournament.display_tournaments(tournament_serialized, player_serialized)
            player_serialized.clear()
            self.home_menu_controller()
        # Choose a tournament
        if entry == "2":
            self.display_tournament.choose_a_tournament()
            valid_choice = True
            while valid_choice:
                print("Entrez le numéro correspondant")
                choice_id = input("-->")

                for tournament in tournament_objects:
                    if int(choice_id) == tournament.doc_id:
                        tournament_object = self.tournament_database.get(doc_id=int(choice_id))
                        tournament_object = self.tournament.unserialized(tournament_object)
                        if tournament_object.list_of_tours == []:
                            print("\nLe tournoi n'a pas encore eu lieu, vous ne pouvez pas afficher les résultats\n")
                            time.sleep(1)

                        else:
                            entry = self.create_menu(self.create_menu.tournaments_report_menu_2)

                            # Display the players
                            if entry == "1":
                                entry = self.create_menu(self.create_menu.players_report_menu)

                                # Display the players alphabetical
                                if entry == "1":
                                    for id in tournament_object.players_ids:
                                        player = self.players_database.get(doc_id=int(id))
                                        player_serialized.append(self.player.unserialized(player))
                                    player_serialized.sort(key=attrgetter("last_name"))
                                    self.display_player.display_alphabetical(player_serialized)
                                    player_serialized.clear()
                                    TournamentReport.__call__(self)

                                # Display the players by ranking
                                if entry == "2":
                                    for id in tournament_object.players_ids:
                                        player = self.players_database.get(doc_id=int(id))
                                        player_serialized.append(self.player.unserialized(player))
                                    player_serialized.sort(key=attrgetter("ranking"))
                                    self.display_player.display_ranking(player_serialized)
                                    player_serialized.clear()
                                    input("Appuyez sur une touche pour revenir au menu rapport de tournoi")
                                    TournamentReport.__call__(self)

                            # Display the tours
                            if entry == "2":
                                for tour in tournament_object.list_of_tours:
                                    tr = tour_table.get(doc_id=tour)
                                    print(f"{tr['Nom']} - Début: {tr['Debut']} - Fin : {tr['Fin']}\n")
                                input("Appuyez sur une touche pour revenir au menu rapport de tournoi")
                                TournamentReport.__call__(self)

                            # Display the matchs
                            if entry == "3":
                                for tour in tournament_object.list_of_tours:
                                    tr = tour_table.get(doc_id=tour)
                                    print(f"{tr['Nom']} :")
                                    for match in tr['Matchs']:
                                        player_1 = match[0][0]
                                        player_1 = self.players_database.get(doc_id=player_1)
                                        score_player_1 = match[0][1]
                                        player_2 = match[1][0]
                                        player_2 = self.players_database.get(doc_id=player_2)
                                        score_player_2 = match[1][1]
                                        print(f"{player_1['Nom']} {player_1['Prenom']} CONTRE "
                                              f"{player_2['Nom']} {player_2['Prenom']}\n"
                                              f"Score : {score_player_1} -- {score_player_2}\n")

                                input("Appuyez sur une touche pour revenir au menu rapport de tournoi")
                                TournamentReport.__call__(self)

                            # Go to main menu
                            if entry == "4":
                                valid_choice = False
                                self.home_menu_controller()

        # Go to main menu
        if entry == "3":
            valid_choice = False
            self.home_menu_controller()

        print("Vous devez entrer le numéro correspondant au tournoi")
