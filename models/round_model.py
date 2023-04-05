from views import view_main
from models.match_model import Match


class Tour:
    """
    Each round is a list of matches. Each match consists of a pair of players with a results
    field for each player. When a round is over, the tournament manager enters the results of
    each match before generating the next pairs.

    Tour instances should be stored in a list on the tournament instance they belong to.

    """

    # TOUR_NUMBER = 1

    def __init__(
        self, name=None, begin_time=None, end_time=None, list_of_finished_matchs=None
    ):
        self.name = name
        self.begin_time = begin_time
        self.end_time = end_time
        self.list_of_finished_matchs = list_of_finished_matchs
        self.list_of_tours = []

    def serialized(self):
        tour_infos = {}
        tour_infos["Nom"] = self.name
        tour_infos["Debut"] = self.begin_time
        tour_infos["Fin"] = self.end_time
        tour_infos["Matchs"] = self.list_of_finished_matchs
        return tour_infos

    def unserialized(self, serialized_tour):
        name = serialized_tour["Nom"]
        begin_time = serialized_tour["Debut"]
        end_time = serialized_tour["Fin"]
        list_of_finished_matchs = serialized_tour["Matchs"]
        return Tour(name, begin_time, end_time, list_of_finished_matchs)

    def __repr__(self):
        return f"{self.name} - Début : {self.begin_time}. Fin : {self.end_time}."

    def run(self, sorted_players_list, tournament_object):
        self.view = view_main.TourDisplay()
        self.list_of_tours = []
        self.list_of_finished_matchs = []
        self.name = "Tour " + str(len(tournament_object.list_of_tours) + 1)
        # Tour.TOUR_NUMBER += 1

        self.begin_time, self.end_time = self.view.display_tournament_time()

        # while there are players in the list, add instances of 'match' to the 'list_of_tours' list
        while len(sorted_players_list) > 0:
            match_instance = Match(
                self.name, sorted_players_list[0], sorted_players_list[1]
            )
            Match.MATCH_NUMBER += 1
            self.list_of_tours.append(match_instance)
            del sorted_players_list[0:2]

        self.view.display_tour(self.name, self.list_of_tours)

        for match in self.list_of_tours:
            valid_score_player_1 = False
            while not valid_score_player_1:
                try:
                    score_player_1 = input(f"Entrez le score de {match.player_1} :")
                    float(score_player_1)
                except Exception:
                    print("Vous devez entrer 0, 0.5, ou 1")
                else:
                    match.score_player_1 = float(score_player_1)
                    match.player_1.tournament_score += float(score_player_1)
                    valid_score_player_1 = True

            valid_score_player_2 = False
            while not valid_score_player_2:
                try:
                    score_player_2 = input(f"Entrez le score de {match.player_2} :")
                    float(score_player_2)
                except Exception:
                    print("Vous devez entrer 0, 0.5, ou 1")
                else:
                    match.score_player_2 = float(score_player_2)
                    match.player_2.tournament_score += float(score_player_2)
                    valid_score_player_2 = True

            self.list_of_finished_matchs.append(
                (
                    [match.player_1.player_id, match.score_player_1],
                    [match.player_2.player_id, match.score_player_2],
                )
            )

        # Returns the round instance
        return Tour(
            self.name, self.begin_time, self.end_time, self.list_of_finished_matchs
        )
