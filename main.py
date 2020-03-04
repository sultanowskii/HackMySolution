import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from main_ui import Ui_MainWindow
from player import Player
import json


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.curr_level = 0
        self.setupUi(self)
        self.INTRO_WIDGETS = [self.input_name, self.label_intro, self.btn_start, self.label_text4]
        self.LEVEL_WIDGETS = [self.input_answer, self.btn_leaderboard, self.btn_solve, self.label_conditions,
                         self.label_solution, self.label_text1, self.label_text1, self.label_text2, self.label_text3]
        for widget in self.LEVEL_WIDGETS:
            widget.setDisabled(True)    # выключаем виджеты уровней
            widget.hide()   # скрываем виджеты уровней
        self.btn_start.clicked.connect(self.start_game)
        self.btn_solve.clicked.connect(self.solve)
        self.btn_leaderboard.clicked.connect(self.open_leaderboard)
        self.player_list = self.get_players()  # при запуске программы она считывает из .json список игроков, создает
        #   для каждого отдельный экземпляр класса Player, и позже сортируется (в методе вызова списка для показа юзеру)

    def solve(self):
        try:
            curr_test = int(self.input_answer.text().strip())
        except:
            return
            #   вывод сообщения об ошибке - введеный тест не является числом.
        pass
        # здесь проверяем два решения

    def open_leaderboard(self):
        self.sort_players()
        pass
        # открываем доску лидеров

    def start_game(self):
        name = self.input_name.text()
        if name == "":
            return
        self.leaderboard.append(Player(name))
        for widget in self.INTRO_WIDGETS:
            widget.setDisabled(True)    # выключаем главного экрана
            widget.hide()   # скрываем виджеты главного экрана
        for widget in self.LEVEL_WIDGETS:
            widget.setDisabled(False)   # включаем виджеты
            widget.show()   # показываем виджеты
        self.next_level()

    def next_level(self):
        self.curr_level += 1
        pass

    def player_comparator(self, player):
        return int(player.score)

    def sort_players(self):
        self.player_list.sort(key=self.player_comparator)

    def get_players(self):
        with open("players.json", "r") as data:
            json_data = json.loads(data.read())
            curr_player_list = []
            for player in json_data["players"].keys():
                curr_player_list.append(Player(player, json_data["players"][player]))
        return curr_player_list


app = QApplication(sys.argv)
ex = MainWindow()
ex.show()
sys.exit(app.exec_())
