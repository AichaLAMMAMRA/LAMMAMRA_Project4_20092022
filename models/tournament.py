from models.round import Round


class Tournament:
    def __init__(self, tournament_name, location, tournament_date, time_control, players_ids, number_of_rounds=4, Description=""):
        self.tournament_name = tournament_name
        self.location = location
        self.tournament_date = tournament_date
        self.time_control = time_control
        self.players_ids = players_ids
        self.number_of_rounds = number_of_rounds
        self.list_of_rounds = []
        self.Description = Description

    def __str__(self):
        return f"Tournoi: {self.tournament_name}"

    def create_round(self, round_number):
        players_pairs = self.create_players_pairs(current_round=round_number)
        round = Round("Round " + str(round_number + 1), players_pairs)
        self.list_of_rounds.append(round)

    def create_players_pairs(self, current_round):

        # Premier round : on trie les joueurs par rank
        if current_round == 0:
            sorted_players = sorted(self.players_ids, key=lambda x: x.rank, reverse=True)

        # Rounds suivant :on les trie par rapport à leur score total
        else:
            sorted_players = []
            score_sorted_players = sorted(self.players_ids, key=lambda x: x.total_score, reverse=True)

          
            for i, player in enumerate(score_sorted_players):
                try:
                    sorted_players.append(player)
                except player.total_score == score_sorted_players[i+1].total_score:
                    if player.rank > score_sorted_players[i+1].rank:
                        hi_player = player
                        lo_player = score_sorted_players[i+1]
                    else:
                        hi_player = score_sorted_players[i+1]
                        lo_player = player
                    sorted_players.append(hi_player)
                    sorted_players.append(lo_player)
                except IndexError:
                    sorted_players.append(player)

        sup_part = sorted_players[len(sorted_players)//2:]
        inf_part = sorted_players[:len(sorted_players)//2]

        players_pairs = []

        for i, player in enumerate(sup_part):
            a = 0
            while True:
                try:
                    player2 = inf_part[i+a]

                except IndexError:
                    player2 = inf_part[i]
                    players_pairs.append((player, player2))

                    player.played_with.append(player2)
                    player2.played_with.append(player)
                    break

                if player in player2.played_with:
                    a += 1
                    continue

                else:
                    players_pairs.append((player, player2))
                    player.played_with.append(player2)
                    player2.played_with.append(player)
                    break

        return players_pairs

    def get_rankings(self, by_score=True):

        if by_score:
            sorted_players = sorted(self.players_ids, key=lambda x: x.tournament_score, reverse=True)
        else:
            sorted_players = sorted(self.players_ids, key=lambda x: x.rank, reverse=True)

        return sorted_players


    def get_serialized_tournament(self, save_rounds=False):
        tournament_infos = {}
        tournament_infos['tournament_name'] = self.tournament_name
        tournament_infos['location'] = self.location
        tournament_infos['tournament_date'] = self.tournament_date
        tournament_infos['time_control'] = self.time_control
        tournament_infos['players_ids'] = [player.get_serialized_player(save_turnament_score=True) for player in self.players_ids]
        tournament_infos['number_of_rounds'] = self.number_of_rounds
        tournament_infos['list_of_rounds '] = [round.get_serialized_round() for round in self.list_of_rounds]
        tournament_infos['Description'] = self.Description

        if save_rounds:
            tournament_infos["list_of_rounds"] = [round.get_serialized_round() for round in self.list_of_rounds]

        return tournament_infos
