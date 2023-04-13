

class MenuViews:

    def __init__(self):
        pass

    @staticmethod
    def input_prompt_txt(option):
        input(f"\n{option} ")
    
    @staticmethod
    def input_prompt(option):

        return input(f"\n{option} ")
         

    @staticmethod
    def input_error():
        print(f"\n- Erreur de saisie, veuillez entrer une option valide.")

    @staticmethod
    def print_prompt(option):
        print(f"\n {option} ")

  