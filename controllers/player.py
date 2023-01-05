from models.player import Player
from views.player import CreatePlayer


def create_player():

    # Récupération des infos du joueur
    user_entries = CreatePlayer().display_menu()

    # Création du joueur
    player = Player(
        user_entries['name'],
        #user_entries['first_name'],
        #user_entries['dob'],
        #user_entries['sex'],
        user_entries['total_score'],
        user_entries['rank'])

    # serialization:
    serialized_player = player.get_serialized_player()
    print(serialized_player)
    
    return player

