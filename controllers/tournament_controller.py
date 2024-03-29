import time
import copy
from operator import itemgetter
from operator import attrgetter
import pandas as pd
from controllers import main_control
from controllers import create_menus
from models import tournament_model
from models import player_model
from models import round_model
from views import view_main, view


class CreateTournamentController:
    """Create a tournament with entering all the details, then save it in the database"""

    def __init__(self):
        self.create_menu = create_menus.CreateMenus()
        self.tournament_values = []
        self.players_in_tournament = []
        self.players_ids = []
        self.menu = view.MenuViews()
        self.players_serialized = []
        self.player = player_model.Player()
        self.home_menu_controller = main_control.HomeMenuController()
        self.tournament = tournament_model.Tournament()

    def __call__(self):
        self.menu.create_tournament_header()
        self.tournament_values.append(self.add_tournament_name())
        self.tournament_values.append(self.add_location())
        self.tournament_values.append(self.add_description())
        self.tournament_values.append(self.add_tournament_date())
        self.tournament_values.append(self.add_number_of_rounds())
        self.tournament_values.append(self.add_time_control())
        self.add_players_to_tournament()
        self.tournament_values.append(self.players_in_tournament)
        self.tournament.add_to_database(self.tournament_values)
        self.home_menu_controller()

    def add_tournament_name(self):
        valid_tournament_name = False
        while not valid_tournament_name:
            tournament_name = self.menu.input_prompt_txt("Nom du tournoi:")
            if tournament_name != "":
                valid_tournament_name = True
            else:
                self.menu.input_error()
        return tournament_name

    def add_location(self):
        valid_location = False
        while not valid_location:
            location = self.menu.input_prompt_txt("- Lieu de tournoi:")
            if location != "":
                valid_location = True
            else:
                self.menu.input_error()
        return location

    def add_description(self):
        description = self.menu.input_prompt_txt("- Description au tournoi:")
        return description

    def add_tournament_date(self):
        date_list = []
        valid_day = False
        while not valid_day:
            self.birth_day = self.menu.input_prompt("- Jour du tournoi:")
            if self.birth_day.isdigit() and len(self.birth_day) == 2 and int(self.birth_day) < 32:
                valid_day = True
                date_list.append(self.birth_day)
            else:
                self.menu.input_error()
        valid_month = False
        while not valid_month:
            self.birth_month = self.menu.input_prompt("-Mois du tournoi (En chiffre): ")
            if self.birth_month.isdigit() and len(self.birth_month) == 2 and int(self.birth_month) < 13:
                valid_month = True
                date_list.append(self.birth_month)
            else:
                self.menu.input_error()
        valid_year = False
        while not valid_year:
            self.birth_year = self.menu.input_prompt("- Aannée du tournoi: ")
            if self.birth_year.isdigit() and len(self.birth_year) == 4:
                valid_year = True
                date_list.append(self.birth_year)
            else:
                self.input_error()

        return f"{date_list[0]}/{date_list[1]}/{date_list[2]}"

    def add_number_of_rounds(self):
        number_of_rounds = 4
        self.menu.print_prompt("- Souhaitez-vous changer ce nombre ? : (4 par défaut)\n")
        valid_number = False
        while not valid_number:
            self.menu.print_prompt("- 'Y' pour changer\n - 'N' pour continuer")
            choice = self.menu.input_prompt("-->")
            if choice == "Y":
                number_of_rounds = self.menu.input_prompt("- le nombre de rounds ():")
                if number_of_rounds.isdigit():
                    valid_number = True
                else:
                    self.menu.input_error()
            if choice == "N":
                valid_number = True
        return number_of_rounds

    def add_time_control(self):
        self.menu.print_prompt("- Contrôle du temps:")
        time_control = None
        entry = self.create_menu(self.create_menu.time_control_menu)
        if entry == "1":
            time_control = "Bullet"
        if entry == "2":
            time_control = "Blitz"
        if entry == "3":
            time_control = "Coup rapide"
        return time_control

    def add_players_to_tournament(self):
        """Add the ids of the selected players in a list, en return the list"""
        view_main.ClearScreen()
        id_choice = None

        valid_add_player_choice = False
        while not valid_add_player_choice:
            add_player_choice = self.menu.input_prompt("- Voulez-vous ajouter un joueur ?[Y/N]\n "+"-->")
            if add_player_choice == "Y":
                valid_add_player_choice = True
            elif add_player_choice == "N":
                return
            else:
                self.menu.input_error()
        display_players_database = pd.read_json("data/player.json")
        self.menu.print_prompt(display_players_database)
        self.menu.print_prompt("- Vous devez choisir un nombre de joueurs\n")
        self.menu.print_prompt("- Joueurs dans le tournoi : " + str(self.players_ids) + "\n")
        self.menu.print_prompt("- Entrez le numéro du joueur :")
        valid_id = False
        while not valid_id:
            id_choice = self.menu.input_prompt("-->")
            try:
                int(id_choice)
            except Exception:
                self.menu.input_error()
            else:
                valid_id = True
        id_choice = int(id_choice)
        if id_choice <= 0 or id_choice > len(player_model.player_database):
            self.menu.print_prompt("- Vous devez choisir un joueur dans la liste")
            self.menu.input_prompt_txt("- Joueurs dans le tournoi : " + str(self.players_ids) + "\n")
            time.sleep(1)
            self.add_players_to_tournament()
        if id_choice in self.players_ids:
            self.menu.input_prompt_txt("- Vous avez déjà choisi ce joueur dans ce tournoi")
            self.menu.input_prompt_txt("- Joueurs dans le tournoi  " + str(self.players_ids) + "\n")
            time.sleep(1)
            self.add_players_to_tournament()
        self.players_ids.append(id_choice)
        self.menu.input_prompt_txt("- Joueurs dans le tournoi : " + str(self.players_ids) + "\n")
        self.add_players_to_tournament()

        # iterate in id's list, create instance of players, then sort them by ranking.
        for id in self.players_ids:
            player = player_model.player_database.get(doc_id=id)
            self.players_serialized.append(player)
        self.players_serialized.sort(key=itemgetter("Classement"), reverse=True)
        self.players_ids.clear()

        for player in self.players_serialized:
            self.players_ids.append(player.doc_id)
        self.tournament_values.append(self.players_ids.copy())


class StartTournament:
    """Controller who start the tournament, stop when the tournament is ended"""

    MATCHS_PLAYED = []
    TOURS_PLAYED = []

    def __init__(self):
        self.menu = view.MenuViews()

    def __call__(self):
        self.sorted_players = []
        self.tournament_menu_controller = main_control.TournamentMenuController()
        self.tour = round_model.Tour()
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

        self.menu.print_prompt("- Voulez vous sauvegarder et quitter le tournoi en cours ? Y / N\n")
        valid_choice = False
        while not valid_choice:
            choice = self.menu.input_prompt("-->")
            if choice == 'Y':
                valid_choice = True
                self.home_menu_controller()
            elif choice == 'N':
                valid_choice = True
                break
            else:
                self.menu.print_prompt("- Vous devez entrer 'Y' ou 'N'")
                continue

    def load_tournament_statement(self):
        # choose a tournament and calculate the number of remaining rounds
        sorted_players = []
        self.tournament = tournament_model.Tournament()
        self_display_tournament = view_main.LoadTournamentDisplay()
        self.home_menu_controller = main_control.HomeMenuController()
        self.tour = round_model.Tour()
        self.view_final_scores = view_main.EndTournamentDisplay()
        db_tournament = tournament_model.tournament_database
        tours_table = db_tournament.table("tours")
        tours_instances = []

        if self_display_tournament():  # True if there is tournaments already started
            valid_entry = False
            while not valid_entry:
                self.menu.input_prompt("- Entrez le chiffre correspondant au tournoi:")
                choice = self.menu.input_prompt("-->")
                try:
                    int(choice)
                    valid_entry = True
                except Exception:
                    self.menu.input_error()
            else:
                choosen_tournament = tournament_model.tournament_database.get(doc_id=int(choice))
                for tour in choosen_tournament["Tours"]:
                    tour_serialized = tours_table.get(doc_id=tour)
                    tour_object = self.tour.unserialized(tour_serialized)
                    tours_instances.append(tour_object)
                choosen_tournament["Tours"] = tours_instances
                tournament_object = self.tournament.unserialized(choosen_tournament)

        else:
            self.menu.print_prompt("- Pas de tournoi en cours, retour au menu principal")
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
                self.menu.print_prompt("- Entrez le chiffre correspondant au tournoi:")
                choice = self.menu.input_prompt("--> ")
                try:
                    choice.isdigit() is False
                    int(choice) < len(tournament_model.tournament_database)
                    int(choice) <= 0
                except Exception:
                    self.menu.print_prompt("- Vous devez entrer le chiffre correspondant au tournoi")
                else:
                    choosen_tournament = tournament_model.tournament_database.get(doc_id=int(choice))
                    tournament_object = self.tournament.unserialized(choosen_tournament)
                    return tournament_object
        else:
            self.menu.print_prompt("- Pas de tournois créé, veuillez créer un tournoi")
            time.sleep(1)
            self.home_menu_controller()

    def sort_player_first_tour(self, tournament):
        """ return a list of players sorted by ranking"""
        self.player = player_model.Player()
        sorted_players = []
        players_instances = []

        for id in tournament.players_ids:
            player = player_model.player_database.get(doc_id=id)
            player = self.player.unserialized(player)
            players_instances.append(player)

        for player in players_instances:
            player_1 = player
            index_player_1 = players_instances.index(player)

            """ I divide the number of players by 2, and I add the result to the index
            example : For 8 players, I add 4 to the first index,
            player[0] against player [4],
            player[1] against player [5] etc..."""
            if index_player_1 + len(tournament.players_ids) / 2 < len(tournament.players_ids):
                index_player_2 = index_player_1 + int(len(tournament.players_ids) / 2)
                player_2 = players_instances[index_player_2]
                sorted_players.append(player_1)
                sorted_players.append(player_2)
                self.MATCHS_PLAYED.append({player_1.player_id, player_2.player_id})
            else:
                pass

        return sorted_players

    def sort_players_by_score(self, tour_instance):
        """ return a list of players sorted by score"""

        self.player = player_model.Player()
        players = []
        players_sorted_by_score = []
        players_sorted_flat = []
        players_instance = []
        match_to_try = set()

        for match in tour_instance.list_of_finished_matchs:
            for player in match:
                players.append(player)

        players_sorted_by_score = copy.copy(players)

        for player in players_sorted_by_score:
            players_sorted_flat.append(player[0])

        players_sorted_by_score.clear()

        for player_id in players_sorted_flat:
            player = player_model.player_database.get(doc_id=player_id)
            players_instance.append(self.player.unserialized(player))

        # Sort players by score, if score are equals, sort by rank.
        players_instance.sort(key=attrgetter("tournament_score", 'ranking'), reverse=True)

        for player_1 in players_instance:

            if player_1 in players_sorted_by_score:
                continue
            else:
                try:
                    player_2 = players_instance[players_instance.index(player_1) + 1]
                except Exception:
                    break

            match_to_try.add(player_1.player_id)
            match_to_try.add(player_2.player_id)

            while match_to_try in self.MATCHS_PLAYED:  # compare match_to_try with matchs already played
                self.menu.print_prompt(f"Le match {player_1} CONTRE {player_2} a déjà eu lieu")
                time.sleep(1)
                match_to_try.remove(player_2.player_id)
                try:
                    player_2 = players_instance[players_instance.index(player_2) + 1]
                except Exception:
                    break
                match_to_try.add(player_2)
                continue

            else:
                self.menu.print_prompt(f"- Ajout du match {player_1} CONTRE {player_2}")
                players_sorted_by_score.append(player_1)
                players_sorted_by_score.append(player_2)
                players_instance.pop(players_instance.index(player_2))
                self.MATCHS_PLAYED.append({player_1.player_id, player_2.player_id})
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
                self.menu.print_prompt("- Entrez le numéro correspondant:")
                choice_id = self.menu.input_prompt_txt("-->")

                for tournament in tournament_objects:
                    if int(choice_id) == tournament.doc_id:
                        tournament_object = self.tournament_database.get(doc_id=int(choice_id))
                        tournament_object = self.tournament.unserialized(tournament_object)
                        if tournament_object.list_of_tours == []:
                            self.menu.print_prompt("- Tournoi n'a pas encore organisé ")
                            time.sleep(1)
                        else:
                            entry = self.create_menu(self.create_menu.tournaments_report_menu_2)
                            # Display the players
                            if entry == "1":
                                entry = self.create_menu(self.create_menu.players_report_menu)
                                # Display the players alphabetical
                                for id in tournament_object.players_ids:
                                    player = self.players_database.get(doc_id=int(id))
                                    player_serialized.append(self.player.unserialized(player))
                                player_serialized.sort(key=attrgetter("last_name"))
                                self.display_player.display_alphabetical(player_serialized)
                                player_serialized.clear()
                                TournamentReport.__call__(self)

                            # Display the tours
                            if entry == "2":
                                for tour in tournament_object.list_of_tours:
                                    tr = tour_table.get(doc_id=tour)
                                    self.menu.print_prompt(f"{tr['Nom']} - Début: {tr['Debut']} - Fin : {tr['Fin']}\n")
                                self.menu.input_prompt_txt("Appuyez sur une touche pour revenir rapport de tournoi")
                                TournamentReport.__call__(self)

                            # Display the matchs
                            if entry == "3":
                                for tour in tournament_object.list_of_tours:
                                    tr = tour_table.get(doc_id=tour)
                                    self.menu.print_prompt(f"{tr['Nom']} :")
                                    for match in tr['Matchs']:
                                        player_1 = match[0][0]
                                        player_1 = self.players_database.get(doc_id=player_1)
                                        score_player_1 = match[0][1]
                                        player_2 = match[1][0]
                                        player_2 = self.players_database.get(doc_id=player_2)
                                        score_player_2 = match[1][1]
                                        self.menu.print_prompt(f"{player_1['Nom']} {player_1['Prenom']} CONTRE "
                                                               f"{player_2['Nom']} {player_2['Prenom']}\n"
                                                               f"Score : {score_player_1} -- {score_player_2}\n")

                                self.menu.input_prompt_txt("- Appuyez sur une touche pour revenir rapport de tournoi")
                                TournamentReport.__call__(self)

                            # Go to main menu
                            if entry == "4":
                                valid_choice = False
                                self.home_menu_controller()

        # Go to main menu
        if entry == "3":
            valid_choice = False
            self.home_menu_controller()

        self.menu.print_prompt("- Vous devez entrer le numéro correspondant au tournoi")
