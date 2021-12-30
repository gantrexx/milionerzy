import json
import random
import os
import time

prize = [500, 1000, 2000, 5000, 10000, 20000, 40000, 75000, 125000, 250000, 500000, 1000000]

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Question:
    def __init__(self, id, data, answers, correct):
        self.id = id
        self.data = data
        self.answers = answers
        self.correct = correct

    def __str__(self):
        # convert to string
        only_for_correct = {
        0: "A",
        1: "B",
        2: "C",
        3: "D",
        }
        return f"{self.data}\n A: {self.answers[0]} \n B: {self.answers[1]} \n C: {self.answers[2]} \n D: {self.answers[3]}\n correct: {only_for_correct[self.correct]}\n "


class Game:
    def __init__(self, filename, user="", game_data={}):
        self.questions = {}
        f = open(filename)
        data = json.load(f)
        for id, q in enumerate(data['pytania']):
            correct = 0
            if q['odp_poprawna'] == 'A':
                correct = 0
            elif q['odp_poprawna'] == 'B':
                correct = 1
            elif q['odp_poprawna'] == 'C':
                correct = 2
            elif q['odp_poprawna'] == 'D':
                correct = 3
            self.questions[id] = Question(id, q['tresc'], q['odp'], correct)
        f.close()
        if user:
            self.user = user
            self.n = 0
            self.available_rescue = {
                "call friend": True,
                "50/50": True,
                "change": True,
            }
            self.used_questions = []
        elif game_data:
            print(game_data)
            self.user=game_data["user"]
            self.n=game_data["n"]
            self.available_rescue=game_data["available_rescue"]
            self.used_questions=game_data["used_questions_id"]
            self.chosen_question=game_data["chosen_question_id"]

    def check_answer(self, response):
        # checking correct answer
        mapping = {
            "A": 0,
            "B": 1,
            "C": 2,
            "D": 3,
        }

        if mapping[response] == self.chosen_question.correct:
            return True
        return False

    def pick_question(self):
        while True:
            value = random.randint(0,len(self.questions)-1)
            if value in self.used_questions:
                continue
            else:
                self.used_questions.append(value)
                return self.questions[value]

    def call_friend(self):
        shot = random.uniform(0,1)
        level = 0.6

        if shot <= level:
            return self.chosen_question.correct
        else:
            return (self.chosen_question.correct + 1) % len(self.chosen_question.answers)

    def game_save(self):
        game_save = open('game_save.json', 'r')
        saves=json.load(game_save)
        game_save.close()

        game_save = open('game_save.json', 'w')
        save={
        "user": self.user,
        "n": self.n,
        "available_rescue": self.available_rescue,
        "used_questions_id": self.used_questions,
        "chosen_question_id": self.chosen_question.id,
        }

        saves["dumps"][self.user]=save
        json.dump(saves, game_save, indent = 6)
        game_save.close()

    def game_del(self):
        game_save = open('game_save.json', 'r')
        saves=json.load(game_save)
        game_save.close()

        game_save = open('game_save.json', 'w+')

        del saves["dumps"][self.user]
        json.dump(saves, game_save, indent = 6)
        game_save.close()

    def interprate(self):
        while True:
            response=input("Twój wybór: ")
            response=response.upper()
            if response == "A" or response == "B" or response == "C" or response == "D":            
                if self.check_answer(response):
                    self.n += 1
                    print(f'{bcolors.OKGREEN} Dobrze! {bcolors.ENDC}')
                    time.sleep(1)
                    return True
                else:
                    print(f'{bcolors.FAIL}Koniec gry!{bcolors.ENDC}')
                    print(f'Odpowiedziałeś na {self.n} pytan.')
                    print(f'Poprawna odpowiedź to: {self.chosen_question.answers[self.chosen_question.correct]}.')
                    user_erase=self.game_del()
                    if self.n > 6:
                        print(f'Wygrałeś {prize[6]} złotych.')
                    elif self.n > 1:
                        print(f'Wygrałeś {prize[1]} złotych.')
                    else:
                        print(f'Nie mosz nawet na bilet!')
                    return False
            elif response==str(1):
                if not self.available_rescue["change"]:
                    print("To koło nie jest dostępne")
                    continue
                self.available_rescue["change"]=False
                print("Wybrałeś wymiane pytania")
                return True
            elif response==str(2):
                if not self.available_rescue["call friend"]:
                    print("To koło nie jest dostępne")
                    continue
                self.available_rescue["call friend"]=False
                print("Wybrałeś telefon do przyjaciela")
                friend_suggestion=self.call_friend()
                print(f'Przyjaciel sugeruje: {self.chosen_question.answers[friend_suggestion]}')
            elif response==str(3):
                if not self.available_rescue["50/50"]:
                    print("To koło nie jest dostępne")
                    continue
                self.available_rescue["50/50"]=False
                wrong_tip=random.randint(1,2)
                self.mapping_int_to_letter = {
                0: "A",
                1: "B",
                2: "C",
                3: "D",
                }

                if wrong_tip==1:
                    print(f'Po odrzuceniu dwóch błędnych odpowiedzi pozostały do wyboru: {self.mapping_int_to_letter[self.chosen_question.correct]} {self.mapping_int_to_letter[(self.chosen_question.correct + 1) % len(self.chosen_question.answers)]}')
                else:
                    print(f'Po odrzuceniu dwóch błędnych odpowiedzi pozostały do wyboru: {self.mapping_int_to_letter[(self.chosen_question.correct + 1) % len(self.chosen_question.answers)]} {self.mapping_int_to_letter[self.chosen_question.correct]}')          


    def play(self):
        while True:
            if self.n == 12:
                print("Wygrałeś miliord!")
                return
            os.system("clear")
            print(f'{bcolors.HEADER} Pytanie nr {self.n + 1} za {prize[self.n]} złotych| {bcolors.ENDC}')
            self.chosen_question=self.pick_question()
            print(f'{bcolors.BOLD}{self.chosen_question}{bcolors.ENDC}')
            print("Dostępne koła ratunkowe:")
            if self.available_rescue["change"]:
                print("1 - zmiana pytania")
            if self.available_rescue["call friend"]:
                print("2 - telefon do przyjaciela")
            if self.available_rescue["50/50"]:
                print("3 - pół-na-pół")
            self.game_save()
            if self.interprate():
                continue
            else:
                return

def game_load(user):
    game_save = open('game_save.json', 'r')
    saves=json.load(game_save)
    game_save.close()

    game_save = open('game_save.json', 'w')
    saves["dumps"][user]["loaded"]="1"

    json.dump(saves, game_save, indent = 6)
    game_save.close()

    with open("game_save.json") as game_load:
        load_x=json.load(game_load)
    # game_data=next((item for item in load["dumps"] if item["user"] == user), None)
    print("Wczytuje dane dla: ",user)
    time.sleep(2)
    return load_x["dumps"].get(user,{})

if __name__ == "__main__":
    user=input("Podaj swoje imie: ")
    game_data=game_load(user)
    if game_data:
        game=Game('pytania_wlasne.json',game_data=game_load(user))
    else:
        game=Game('pytania_wlasne.json',user=user)
    game.play()

