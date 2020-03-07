import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from main_ui import Ui_MainWindow
from player import Player
import json
import subprocess
from LeaderBoard import LeaderBoard


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.curr_level = 0
        self.setupUi(self)
        self.INTRO_WIDGETS = [self.input_name, self.label_intro, self.btn_start, self.label_text4]
        self.LEVEL_WIDGETS = [self.input_answer, self.btn_solve, self.label_conditions,
                         self.label_solution, self.label_text1, self.label_text1, self.label_text2, self.label_text3]
        self.attempts = 0
        self.solution = ""  # название файла авторского решения конкретной задачи
        self.solution_dima = ""  # название файла решения Димы
        self.players = self.get_players() # при запуске программы она считывает из .json список игроков, создает
        #   для каждого отдельный экземпляр класса Player, и позже сортируется (в методе вызова списка для показа юзеру)

        self.btn_leaderboard.move(30, 530) # пока так, потом 3 столбиком приклею к меню открытую доску почета
        for widget in self.LEVEL_WIDGETS:
            widget.setDisabled(True)    # выключаем виджеты уровней
            widget.hide()   # скрываем виджеты уровней

        self.btn_start.clicked.connect(self.start_game)
        self.btn_solve.clicked.connect(self.solve)
        self.btn_leaderboard.clicked.connect(self.open_leaderboard)

    def solve(self):
        try:
            input_num = int(self.input_answer.text().strip())   # проверка на то, является ли числом то, что ввел юзер
        except:
            #   вывод сообщения об ошибке - введеный тест не является числом.
            return
        ca = subprocess.run(["python", f"data/levels/{str(self.curr_level)}/{self.solution}"], input=str(input_num), encoding="utf-8", stdout=subprocess.PIPE)
        da = subprocess.run(["python", f"data/levels/{str(self.curr_level)}/{self.solution_dima}"], input=str(input_num), encoding="utf-8", stdout=subprocess.PIPE)
        if ca.stdout == da.stdout:
            self.attempts += 1
            if self.attempts == 3:
                self.end_game()
            # выводим сообщение, что ответы совпали и кол-во оставшихся попыток на решение
        else:
            self.next_level()

    def open_leaderboard(self):
        self.sort_players()
        top10 = []
        for i in range(min(len(self.players), 10)):
            top10.append(self.players[i])
        self.Leaderboard = LeaderBoard(top10)
        self.Leaderboard.show()
        # открываем доску лидеров

    def start_game(self):
        name = self.input_name.text()
        if name == "":
            return
        self.players.append(Player(name))

        with open('data/json/players.json') as f:
            data = json.load(f)
        data["players"][name] = 0
        with open('data/json/players.json', 'w') as f:
            f.write(json.dumps(data, ensure_ascii=False, indent=4))

        self.btn_leaderboard.move(1000, 10) # уберу
        for widget in self.INTRO_WIDGETS:
            widget.setDisabled(True)    # выключаем главного экрана
            widget.hide()   # скрываем виджеты главного экрана
        for widget in self.LEVEL_WIDGETS:
            widget.setDisabled(False)   # включаем виджеты
            widget.show()   # показываем виджеты

        # ENTER HERE TURNING OFF END_WIDGETS

        self.next_level()

    def end_game(self):
        pass    # не забудь все обнулить! (после подсчета очков и занесения их в доску почета)

    def next_level(self):
        self.curr_level += 1
        self.attempts = 0
        self.load_level()

    def player_comparator(self, player):
        return int(player.score)

    def sort_players(self):
        self.players.sort(key=self.player_comparator, reverse=True)

    def get_players(self):
        with open("data/json/players.json", "r") as data:
            json_data = json.loads(data.read())
            curr_player_list = []
            for player in json_data["players"].keys():
                curr_player_list.append(Player(player, json_data["players"][player]))
        return curr_player_list

    def load_level(self):
        with open("data/json/levels.json", "r") as data:
            json_data = json.loads(data.read())["levels"][str(self.curr_level)]
            conditions_text = f"data/levels/{str(self.curr_level)}/" + json_data["conditions_text"]
            solution_dima_text = f"data/levels/{str(self.curr_level)}/" + json_data["solution_dima"]
            with open(conditions_text, 'r', encoding='utf-8') as f:
                self.label_conditions.setText(f.read())
            with open(solution_dima_text, 'r', encoding='utf-8') as f:
                self.label_solution.setText(f.read())
            self.solution = json_data["solution"]
            self.solution_dima = json_data["solution_dima"]


app = QApplication(sys.argv)
ex = MainWindow()
ex.show()
sys.exit(app.exec_())
