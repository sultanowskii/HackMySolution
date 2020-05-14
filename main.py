import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from main_ui import Ui_MainWindow
from player import Player
import json
import subprocess
from Message import Message
import datetime
from random import randint


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.curr_level = 0
        self.setupUi(self)
        self.INTRO_WIDGETS = [self.input_name, self.label_intro, self.btn_start, self.label_text4]
        self.LEVEL_WIDGETS = [self.input_answer, self.btn_solve, self.label_conditions,
                              self.label_solution, self.label_text1, self.label_text1, self.label_text2, self.label_text3]
        self.END_WIDGETS = [self.label_end, self.btn_newgame]
        self.player_labels = [self.lbl1, self.lbl2, self.lbl3, self.lbl4, self.lbl5, self.lbl6, self.lbl7, self.lbl8,
                              self.lbl9, self.lbl10]
        self.attempts = 0
        self.curr_score = 0
        self.curr_name = ""
        self.start_level_time = None
        self.solution = ""  # название файла авторского решения конкретной задачи
        self.solution_dima = ""  # название файла решения Димы
        self.players = self.get_players()  # при запуске программы она считывает из .json список игроков, создает
        #   для каждого отдельный экземпляр класса Player, и позже сортируется (в методе вызова списка для показа юзеру)
        self.level_count = 0
        self.max_score_in30s = self.getMaxScore()
        for widget in self.LEVEL_WIDGETS:
            widget.setDisabled(True)
            widget.hide()
        for widget in self.END_WIDGETS:
            widget.setDisabled(True)
            widget.hide()
        self.update_leaderboard()
        self.btn_newgame.clicked.connect(self.restart)
        self.btn_start.clicked.connect(self.start_game)
        self.btn_solve.clicked.connect(self.solve)

    def solve(self):
        try:
            input_n = self.input_answer.text().split(" ")
            for num in input_n:
                int(num)
        except:
            self.m = Message("Введите число/числа")
            self.m.show()
            return
        ca = subprocess.run(["python", f"data/levels/{str(self.curr_level)}/{self.solution}"],
                            input=str('\n'.join(input_n)), encoding="utf-8", stdout=subprocess.PIPE)
        da = subprocess.run(["python", f"data/levels/{str(self.curr_level)}/{self.solution_dima}"],
                            input=str('\n'.join(input_n)), encoding="utf-8", stdout=subprocess.PIPE)
        self.attempts += 1
        if ca.stdout == da.stdout:
            self.m = Message(
                f"Ответы совпали!\nОтвет авторского решения:\n{str(ca.stdout)}Ответ Владика: {str(da.stdout)}")
            self.m.show()
            self.input_answer.setText("")
            if self.attempts == 3:
                self.curr_level -= 1
                self.end_game()
        else:
            self.m = Message(f"Уровень пройден!\nОтвет авторского решения:\n{str(ca.stdout)}Ответ "
                             f"Владика: {str(da.stdout)}")
            self.m.show()
            if self.curr_level != 0:
                self.curr_score += self.getValueFromLevel() * self.getValueFromTime(self.start_level_time,
                                                                                    datetime.datetime.now()) * \
                                                                                    (4 - self.attempts) * 10
            if self.curr_level == self.level_count:
                self.end_game()
            else:
                self.next_level()

    def update_leaderboard(self):
        self.sort_players()
        top10 = []
        for i in range(min(len(self.players), 10)):
            top10.append(self.players[i])
        for i in range(len(top10)):
            self.player_labels[i].setText(f'{i + 1}. {self.getColorOfPlayer(top10[i])} - {top10[i].score}')
            self.player_labels[i].resize(self.player_labels[i].sizeHint())
            self.player_labels[i].show()

    def start_game(self):
        self.curr_name = self.input_name.text().strip()
        if self.curr_name == "":
            self.m = Message("Введите никнейм")
            self.m.show()
            self.input_name.setText('')
            return
        elif len(self.curr_name) < 3:
            self.m = Message("Никнейм слишком короткий! (минимум 3\nсимвола)")
            self.m.show()
            self.input_name.setText('')
            return
        elif len(self.curr_name) > 15:
            self.m = Message("Никнейм слишком длинный! (максимум 14\nсимволов)")
            self.input_name.setText('')
            self.m.show()
            return
        self.players.append(Player(self.curr_name))

        with open('data/json/players.json') as f:
            data = json.load(f)
        data["players"][self.curr_name] = 0
        with open('data/json/players.json', 'w') as f:
            f.write(json.dumps(data, ensure_ascii=False, indent=4))
        self.players[-1].score = self.curr_score
        self.update_leaderboard()
        for widget in self.INTRO_WIDGETS:
            widget.setDisabled(True)  # выключаем главного экрана
            widget.hide()  # скрываем виджеты главного экрана
        for widget in self.LEVEL_WIDGETS:
            widget.setDisabled(False)  # включаем виджеты
            widget.show()  # показываем виджеты
        for widget in self.END_WIDGETS:
            widget.setDisabled(True)
            widget.hide()

        self.next_level()

    def end_game(self):
        for widget in self.INTRO_WIDGETS:
            widget.setDisabled(True)
            widget.hide()
        for widget in self.LEVEL_WIDGETS:
            widget.setDisabled(True)
            widget.hide()
        for widget in self.END_WIDGETS:
            widget.setDisabled(False)
            widget.show()

        with open('data/json/players.json') as f:
            data = json.load(f)
        data["players"][self.curr_name] = self.curr_score
        with open('data/json/players.json', 'w') as f:
            f.write(json.dumps(data, ensure_ascii=False, indent=4))
        self.players[-1].score = self.curr_score
        self.update_leaderboard()
        self.label_end.setText(f"Игра окончена. Ваш результат: {self.curr_score}. Вы прошли уровней: {self.curr_level}")

    def restart(self):
        self.curr_name = ""
        self.curr_level = 0
        self.curr_score = 0
        self.attempts = 0
        for widget in self.INTRO_WIDGETS:
            widget.setDisabled(False)
            widget.show()
        for widget in self.LEVEL_WIDGETS:
            widget.setDisabled(True)
            widget.hide()
        for widget in self.END_WIDGETS:
            widget.setDisabled(True)
            widget.hide()
        self.input_name.setText("")

    def next_level(self):
        self.input_answer.setText("")
        self.curr_level += 1
        self.attempts = 0
        self.load_level()
        self.start_level_time = datetime.datetime.now()

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
            with open(solution_dima_text, 'r', encoding='utf-8') as f:
                self.label_solution.setText(f.read())
            self.solution = json_data["solution"]
            self.solution_dima = json_data["solution_dima"]
            self.input_nums = json_data["input_nums"]
            input_n = []
            verdict = 1
            while verdict != 0:
                for _ in range(self.input_nums):
                    input_n.append(str(randint(-20, 21)))
                ca = subprocess.run(["python", f"data/levels/{str(self.curr_level)}/{self.solution}"],
                                    input=str('\n'.join(input_n)), encoding="utf-8", stdout=subprocess.PIPE)
                verdict = ca.returncode
            with open(conditions_text, 'r', encoding='utf-8') as f:
                self.label_conditions.setText(
                    f.read() + f"""\n\nПример:\nВходные данные: {' '.join(input_n)}\nВыходные данные: {ca.stdout}""")

    def getColorOfPlayer(self, player):  # делает ник цветным в зависимости от рейтинга игрока (как на CF)
        if player.score >= int(self.max_score_in30s / 10 * 8):
            return f"""<font color="black">{player.name[0:1]}</font><font color="red">{player.name[1:]}</font>"""
        elif player.score >= int(self.max_score_in30s / 1000 * 625):
            return f"""<font color="red">{player.name}</font>"""
        elif player.score >= int(self.max_score_in30s / 10 * 5):
            return f"""<font color="orange">{player.name}</font>"""
        elif player.score >= int(self.max_score_in30s / 10 * 4):
            return f"""<font color="purple">{player.name}</font>"""
        elif player.score >= int(self.max_score_in30s / 100 * 25):
            return f"""<font color=blue>{player.name}</font>"""
        elif player.score >= int(self.max_score_in30s / 100 * 20):
            return f"""<font color=#7fffd4>{player.name}</font>"""
        elif player.score >= int(self.max_score_in30s / 10):
            return f"""<font color=#228b22>{player.name}</font>"""
        else:
            return f"""<font color="gray">{player.name}</font>"""

    def getValueFromTime(self, start, end):
        if end - start <= datetime.timedelta(seconds=5):
            return 8
        if end - start <= datetime.timedelta(seconds=15):
            return 7
        elif end - start <= datetime.timedelta(seconds=30):
            return 6
        elif end - start <= datetime.timedelta(seconds=60):
            return 5
        elif end - start <= datetime.timedelta(seconds=120):
            return 4
        elif end - start <= datetime.timedelta(seconds=180):
            return 3
        elif end - start <= datetime.timedelta(seconds=240):
            return 2
        else:
            return 1

    def getValueFromLevel(self):  # значения сложности варьируются от 1 до 3
        with open("data/json/levels.json", "r") as data:
            json_data = json.loads(data.read())["levels"][str(self.curr_level)]
            return int(json_data["difficulty"])

    def getMaxScore(self):
        with open("data/json/levels.json", "r") as data:
            maxx = 0
            data = json.loads(data.read())["levels"]
            # формула максимального кол-ва очков за все уровни (ориентируясь на максимальную скорость решения задачи
            # юзером вдиапазоне от 15 до 30 секунд):
            # 30 (максимальный коэффициент за попытки) * 6 (максимальный коэффициент за 30 секунд) *
            # * x (текущую сложность уровня)
            self.level_count = len(data)
            for i in range(1, len(data) + 1):
                maxx += int(data[str(i)]["difficulty"]) * 30 * 6
            return maxx


app = QApplication(sys.argv)
ex = MainWindow()
ex.show()
sys.exit(app.exec_())
