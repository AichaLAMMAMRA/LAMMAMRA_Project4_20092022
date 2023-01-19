from views.view import View


class CreatePlayer(View):

    def display_menu(self):

        name = input("""Nom du joueur:\n> """)

        rank = self.get_user_entry(
            msg_display="Rang:\n> ",
            msg_error="Veuillez entrer une valeur numérique valide.",
            value_type="numeric"
        )

        print(f"Joueur  {name} créé.")
        #print(f"Joueur {first_name} {name} créé.")

        return {
                "name": name,
                "total_score": 0,
                "rank": rank,
                }
        '''
         return {
                "name": name,
                #"first_name": first_name,
                #"dob": dob,
                #"sex": sex,
                "total_score": 0,
                "rank": rank,
                }
        '''

        #first_name = input("""Prénom du joueur:\n> """)

    '''#dob = self.get_user_entry(
            msg_display="Date de naissance (format DD-MM-YYYY):\n> ",
            msg_error="Veuillez entrer une date au format valide: DD-MM-YYYY",
            value_type="date"
        )

        sex = self.get_user_entry(
            msg_display="Sexe (H ou F):\n> ",
            msg_error="Veuillez entrer H ou F",
            value_type="selection",
            assertions=["H", "h", "F", "f"]
        ).upper()'''



