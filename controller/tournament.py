from models.tournament import Tournament
from views.view import View
from views.tournament import CreateTournament
from controller.player import create_player


def create_tournament():

    menu = View()
    # Récupération des infos du tournoi
    user_entries = CreateTournament().display_menu()

    # Choix chargement joueurs:
    user_input = menu.get_user_entry(
        msg_display="Que faire ?\n0 - Créer des joueurs\n1 - Charger des joueurs\n> ",
        msg_error="Entrez un choix valide.",
        value_type="selection",
        assertions=["0", "1"]
    )

    # Chargement des joueurs
    if user_input == "0":
        print(f"Création de {str(user_entries['nb_players'])} joueurs.")
        players = []
        while len(players) < user_entries['nb_players']:
            players.append(create_player())

    # Creation du tournoi
    tournament = Tournament(
        user_entries['name'],
        user_entries['place'],
        user_entries['date'],
        user_entries['time_control'],
        players,
        user_entries['nb_rounds'],
        user_entries['desc'])

   
    return tournament


def play_tournament(tournament, new_tournament_loaded=False):

    menu = View()
    print()
    print(f"Début du tournoi {tournament.name}")
    print()

    while True:

        a = 0
        if new_tournament_loaded:
            for round in tournament.rounds:
                if round.end_date == "":
                    a += 1
            nb_rounds_to_play = tournament.nb_rounds - a
            new_tournament_loaded = False
        else:
            nb_rounds_to_play = tournament.nb_rounds

        for i in range(nb_rounds_to_play):

            # Création du round
            tournament.create_round(round_number=i+a)

      
            current_round = tournament.rounds[-1]
            print()
            print(current_round.start_date + " : Début du " + current_round.name)

            # Round terminé, on passe au round suivant
            while True:
                print()
                user_input = menu.get_user_entry(
                    msg_display="Que faire ?\n"
                                "0 - Round suivant\n",
                    msg_error="Veuillez faire un choix.",
                    value_type="selection",
                    assertions=["0", "1", "2", "3", "4"]
                )
                print()

                if user_input == "0":
                    current_round.mark_as_complete()
                    break
        else:
            break

    # Sile  tournoi terminé,on retourne les résultats
    rankings = tournament.get_rankings()
    for i, player in enumerate(rankings):
        for t_player in tournament.players:
            if player.name == t_player.name:
                t_player.total_score += player.tournament_score
                t_player.rank = str(i+1)
    return rankings