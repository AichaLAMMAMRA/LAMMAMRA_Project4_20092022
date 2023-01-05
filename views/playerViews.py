from views.view import View



class CreatePlayer(View):

    def display_menu(self):
        name = input("Nom du joueur :\n"
                     ">>> ")

        firstname = input("Prénom du joueur :\n"
                          ">>> ")

        birthday = self.get_user_entry(
            msg_display="Date de naissance (format DD/MM/YYYY) :\n"
                        ">>> ",
            msg_error="Veuillez entrer une date au format valide: DD/MM/YYYY",
            value_type="date"
        )

        gender = self.get_user_entry(
            msg_display="Sexe (H ou F) :\n"
                        ">>> ",
            msg_error="Veuillez entrer H ou F",
            value_type="selection",
            assertions=["H", "h", "F", "f"]
        ).upper()

        rating = self.get_user_entry(
            msg_display="Classement :\n"
                        ">>> ",
            msg_error="Veuillez entrer une valeur numérique valide",
            value_type="numeric"
        )

        print(f"{firstname} {name} a été créé")

        return {
            "name": name,
            "firstname": firstname,
            "birthday": birthday,
            "gender": gender,
            "total_score": 0,
            "rating": rating,
        }


