import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from lb_ui import Ui_Form


class LeaderBoard(QWidget, Ui_Form):
    def __init__(self, top10):
        super().__init__()
        self.setupUi(self)
        self.top10 = top10
        self.labels = [self.lbl1, self.lbl2, self.lbl3, self.lbl4, self.lbl5, self.lbl6, self.lbl7, self.lbl8,
                       self.lbl9, self.lbl10]
        for i in range(len(self.top10)):
            self.labels[i].setText(f'{i + 1}. {self.getColor(top10[i])} - {self.top10[i].score}')

    def getColor(self, player): #   делает ник цветным в зависимости от рейтинга игрока (как на CF)
        if player.score >= 1000:
            return f"""<font color="black">{player.name[0:1]}</font><font color="red">{player.name[1:]}</font>"""
        elif player.score >= 500:
            return f"""<font color="red">{player.name}</font>"""
        elif player.score >= 450:
            return f"""<font color="orange">{player.name}</font>"""
        elif player.score >= 400:
            return f"""<font color="purple">{player.name}</font>"""
        elif player.score >= 300:
            return f"""<font color=blue>{player.name}</font>"""
        elif player.score >= 150:
            return f"""<font color=#7fffd4>{player.name}</font>"""
        else:
            return f"""<font color="gray">{player.name}</font>"""