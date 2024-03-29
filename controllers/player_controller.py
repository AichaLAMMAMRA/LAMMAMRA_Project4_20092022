from operator import attrgetter

from controllers import main_control
from models import player_model
from views import view_main, view
from controllers import create_menus


class CreatePlayerController:
    """Enter all the player's details, then add the player in the database"""
    def __init__(self):
        self.player_values = []
        self.menu = view.MenuViews()
        self.player_keys = ["Nom", "Prénom", "Date de naissance", "Sexe", "Classement"]
        self.home_menu_controller = main_control.HomeMenuController()

    def __call__(self):

        self.user_input = int(self.menu.input_prompt("- Nombre de joueurs à créer:"))
        for i in range(self.user_input):
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
            last_name = self.menu.input_prompt("- Entrez le nom de famille: ")
            if last_name != "":
                valid_last_name = True
            else:
                self.menu.input_error()
        return last_name

    def add_first_name(self):
        valid_first_name = False
        while not valid_first_name:
            first_name = self.menu.input_prompt("- Entrez le prénom: ")
            if first_name != "":
                valid_first_name = True
            else:
                self.menu.input_error()
        return first_name

    def add_birth_details(self):
        birthdate_list = []

        valid_day = False
        while not valid_day:
            self.birth_day = self.menu.input_prompt("- Entrez le jour de naissance: ")
            if self.birth_day.isdigit() and len(self.birth_day) == 2 and int(self.birth_day) < 32:
                valid_day = True
                birthdate_list.append(self.birth_day)
            else:
                self.menu.print_prompt("- Vous devez entrer un nombre à 2 chiffres <= 31")

        valid_month = False
        while not valid_month:
            self.birth_month = self.menu.input_prompt("- Entrez le mois de naissance: (En chiffre) ")
            if self.birth_month.isdigit() and len(self.birth_month) == 2 and int(self.birth_month) < 13:
                valid_month = True
                birthdate_list.append(self.birth_month)
            else:
                self.menu.print_prompt("- Vous devez entrer un nombre à 2 chiffres <= 12")

        valid_year = False
        while not valid_year:
            self.birth_year = self.menu.input_prompt("- Entrez l'année de naissance: ")
            if self.birth_year.isdigit() and len(self.birth_year) == 4 and int(self.birth_year) < 2021:
                valid_year = True
                birthdate_list.append(self.birth_year)
            else:
                self.menu.print_prompt("- Veuillez entrer une année à 4 chiffres (exemple : 1980)")

        return f"{birthdate_list[0]}/{birthdate_list[1]}/{birthdate_list[2]}"

    def add_gender(self):
        valid_gender = False
        validated_gender = None
        while not valid_gender:
            gender = self.menu.input_prompt("Genre du joueur: 'H' pour un homme 'F' pour une femme\n")
            if gender == "H":
                valid_gender = True
                validated_gender = "Homme"
            elif gender == "F":
                valid_gender = True
                validated_gender = "Femme"
            else:
                self.menu.print_prompt("- Vous devez entrer un genre (H ou F)")
        return validated_gender

    def add_ranking(self):
        valid_ranking = False
        while not valid_ranking:
            ranking = self.menu.input_prompt("- Entrez le classement du joueur: ")
            if ranking.isdigit() and int(ranking) >= 0:
                valid_ranking = True
            else:
                self.menu.print_prompt("- Vous devez entrer un nombre entier positif")
        return int(ranking)

    def validate_player(self):
        validated_choice = False
        while not validated_choice:
            self.menu.print_prompt("- Valider ce joueur ?[Y/N] \n")
            choice = self.menu.input_prompt("-->")
            if choice == "Y":
                validated_choice = True
            elif choice == "N":
                main_control.HomeMenuController()
            else:
                self.menu.print_prompt("- Vous devez entrer 'Y' ou 'N'")
        return validated_choice


class PlayerReport:
    """Display the players report"""

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
            self.home_menu_controller()
