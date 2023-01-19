from controllers.tournament import create_tournament, play_tournament
from views.player import CreatePlayer
from views.view import View


class MainDisplay(View):

    def display_main_menu(self):

        while True:
            print()
            user_input = self.get_user_entry(
                msg_display="Que faire ?\n"
                            "0 - Créer un tournoi\n"
                            "1 - Créer des joueurs\n"
                            "q - Quitter\n> ",
                msg_error="Veuillez entrer une valeur valide",
                value_type="selection",
                assertions=["0", "1",  "q"]
            )

            # Creer un tournoi
            if user_input == "0":
                tournament = create_tournament()
                break
           
            # Creer des joueurs
            elif user_input == "1":
                user_input = self.get_user_entry(
                    msg_display="Nombre de joueurs à créer:\n> ",
                    msg_error="Veuillez entrer une valeur numérique valide ",
                    value_type="numeric"
                )
                for i in range(user_input):
                    serialized_new_player = CreatePlayer().display_menu()
            
            else:
                quit()     

          

        # on joue le tournoi
        print()
        user_input = self.get_user_entry(
            msg_display="Que faire ?\n"
                        "0 - Jouer le tournoi\n"
                        "q - Quitter\n> ",
            msg_error="Veuillez entrer une valeur valide",
            value_type="selection",
            assertions=["0", "q"]
        )

        # on récupère les résultats une fois le tournoi terminé
        if user_input == "0":
            rankings = play_tournament(tournament, new_tournament_loaded=True)
        else:
            quit()

        print()
        print(f"Tournoi {tournament.name} terminé !\nRésultats:")
        for i, player in enumerate(rankings):
            print(f"{str(i + 1)} - {player}")

      