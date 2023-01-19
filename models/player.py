



class Player:
    def __init__(self, last_name=None,
                first_name=None, 
                birthdate=None, 
                gender=None, 
                total_score=0, 
                ranking=0
                ):
        self.last_name = last_name
        self.first_name = first_name
        self.birthdate = birthdate
        self.gender = gender
        self.ranking = ranking
        self.tournament_score = 0
        self.player_id = 0

    def __str__(self):
        return f"{self.first_last_name} {self.last_name} [{self.tournament_score} pts]"

    def get_serialized_player(self, save_turlast_nament_score=False):
        player_infos = {}
        player_infos['Nom'] = self.last_name
        player_infos['Prenom'] = self.first_name
        player_infos['Date de naissance'] = self.birthdate
        player_infos['Sexe'] = self.gender
        player_infos['Classement'] = self.ranking
        player_infos['Score'] = self.tournament_score
        player_infos['Id du joueur'] = self.player_id

        if save_turlast_nament_score:
            tournament_score["tournament_score"] = self.tournament_score

        return player_infos