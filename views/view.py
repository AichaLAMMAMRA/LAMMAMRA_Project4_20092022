

class MenuViews:

    def __init__(self):
        pass

    @staticmethod
    def create_tournament_header():
        print("\n" * 1 + "--- NOUVEAU TOURNOI ---")

    @staticmethod
    def input_prompt_txt(option):
        input(f"\n{option}")

    @staticmethod
    def input_prompt(option):
        return input(f"\n{option}")

    @staticmethod
    def input_error():
        print("\n- Erreur de saisie, veuillez entrer une option valide.")

    @staticmethod
    def print_prompt(option):
        print(f"\n {option} ")
