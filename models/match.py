

class Match:

    def __init__(self, name, players_pair):
           
       
        self.player1 = players_pair[0]
        self.score_player1 = 0
        self.player2 = players_pair[1]
        self.score_player2 = 0
        self.winner = None
        self.name = name

    def play_match(self):
        #ptin()
        winner = View().get_user_entry(
            msg_display=f"{self.player_1.firstname} VS {self.player_2.firstname}\n"
                        "Gagnant ?\n"
                        f"0 - {self.player_1.firstname}\n"
                        f"1 - {self.player_2.firstname}\n"
                        "2 - Égalité\n"
                        ">>> ",
            msg_error="Veuillez entrer 0, 1 ou 2.",
            value_type="selection",
            assertions=["0", "1", "2"]
        )
        if winner == "0":
            self.winner = self.player_winner(self.player_1)
            self.score_player_1 += 1
        elif winner == "1":
            self.winner = self.player_winner(self.player_2)
            self.score_player_2 += 1
        elif winner == "2":
            self.winner = self.player_winner(' Égalité ')
            self.score_player_1 += 0.5
            self.score_player_2 += 0.5

        self.player_1.tournament_score += self.score_player_1
        self.player_2.tournament_score += self.score_player_2

    def get_serialized_match(self):
        return {
            "player1": self.player1.get_serialized_player(save_turnament_score=True),
            "score_player1": self.score_player1,
            "player2": self.player2.get_serialized_player(save_turnament_score=True),
            "score_player2": self.score_player2,
            "winner": self.winner,
            "name": self.name
        }

    


        