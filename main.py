import sqlite3
import PyQt5
import sys  # sys нужен для передачи argv в QApplication
import matplotlib.patches
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QVBoxLayout, QTableWidgetItem
# from matplotlib.backends.backend_template import FigureCanvas
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from UI import Ui_MainWindow  # Это наш конвертированный файл дизайна
# pyuic5 UI.ui -o UI.py
import math
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import matplotlib.pyplot as plt
import numpy as np
from scipy import *
from UI_Choose import Ui_Form
from UI_dialog import Ui_Dialog

# GLOBAL
# Wing

l = 0
S = 0
b = 0
b0 = 0
bk = 0
n = 0
cmax = 0
c_ = 0
xc = 0
xc_ = 0
fmax = 0
f_ = 0
a0 = 0
xf = 0
xf_ = 0
xc_degree = 0
x_degree = 0
lamda = 0
Sf = 0
Sf_ = 0
Sgd = 0
Sgd_ = 0
Sgsh = 0
Sgh_ = 0
S_ = 0
lamdaef = 0
caya = 0
Sobd = 0
Sobd_ = 0
xtau_ = 0
cmo = 0
h = 0

# Flap and Mulard
lzak = 0
bzak = 0
bzak_ = 0
Sobzak = 0
Sobzak_ = 0
deltavzl = 0
deltapos = 0
xshzak = 0
bsrzak = 0
hvzl = 0
hpos = 0
Sobpr = 0
Sobpr_ = 0
Flap_type = ''

# Tail
bgo = 0
cgo_ = 0
lgo = 0
Sgo = 0
lamdago = 0
xgo = 0
bv = 0
Sv = 0
bvo = 0
lvo = 0
Svo = 0
cvo_ = 0

# Pylon
bp = 0
cp_ = 0
Sp = 0

# Fuselage
lf = 0
Df = 0
Smf = 0
lamdaf = 0
Ssm = 0
lnf = 0
lamdanf = 0

# Gondola
lgd = 0
Dgd = 0
lamdagd = 0
Ssm_gd = 0
ln_gd = 0
lamdan_gd = 0

lgsh = 0
Dgsh = 0
lamdagsh = 0
Ssm_gsh = 0
ln_gsh = 0
lamdan_gsh = 0

# Common Data
Dv = 0
Fv = 0
Gvzl = 0
V = 0
number = 0
P0 = 0
H = 0
type = ''

# ВЕЛИЧИНЫ ИЗ ГРАФИКОВ
Kx = 0
Kn = 0
Cyamaxprof = 0

# ВЕЛИЧИНЫ ИЗ ТАБЛИЦ
pH = 0  # массовая плотность
aH = 0  # скорость звука
Gm = 0  # полный запас топлива

dCyamax = 0  # по типу закрылка

# CONST
g = 9.8

# ВЫСЧИТАННЫЕ
Mrasch = 0  # число Маха расчетное
Gpol = 0  # полетный вес самолета
Cyamax = 0
da0_vzl = 0
# Вспомогательная кривая
Re = 0
Vmin = 0


# ДИАЛОГОВОЕ ОКНО С РАСЧЕТНЫМИ СХЕМАМИ
class DialogPlan(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.dialog = Ui_Dialog()
        self.dialog.setupUi(self)
        self.setBu()

    def setBu(self):
        self.dialog.buNext.clicked.connect(self.NextPic)

    def NextPic(self):
        if self.dialog.stackedWidget.currentIndex() == 0:
            self.dialog.stackedWidget.setCurrentIndex(1)
        else:
            self.dialog.stackedWidget.setCurrentIndex(0)


# ДИАЛОГОВОЕ ОКНО С ЗАКРЫЛКАМИ
class DialogMechanism(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.dialogM = Ui_Form()
        self.dialogM.setupUi(self)
        self.set()

    def set(self):
        self.dialogM.buClose.clicked.connect(self.ChooseClose)

    def ChooseClose(self):
        global Flap_type
        if self.dialogM.rbWing.isChecked():
            Flap_type = 'Исходное крыло'
        elif self.dialogM.rbSimpleBox.isChecked():
            Flap_type = 'Простой щиток'
        elif self.dialogM.rbBoxCAGI.isChecked():
            Flap_type = 'Щиток ЦАГИ'
        elif self.dialogM.rbSimpleFlap.isChecked():
            Flap_type = 'Простой закрылок'
        elif self.dialogM.rbOneFlap.isChecked():
            Flap_type = 'Однощелевой закрылок'
        elif self.dialogM.rbTwoFlap.isChecked():
            Flap_type = 'Двухщелевой закрылок'
        elif self.dialogM.rnThreeFlap.isChecked():
            Flap_type = 'Трехщелевой закрылок'
        elif self.dialogM.rbFlapFauler.isChecked():
            Flap_type = 'Закрылок Фаулера'
        elif self.dialogM.rbTwoFlapFauler.isChecked():
            Flap_type = 'Двухщелевой закрылок Фаулера'
        elif self.dialogM.rbMulard.isChecked():
            Flap_type = 'Предкрылок'
        self.close()


# ОСНОВНОЕ ПРИЛОЖЕНИЕ
class ExampleApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.main = Ui_MainWindow()
        self.main.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.show()
        self.set()
        self.connection = sqlite3.connect('bd.db')
        self.cursor = self.connection.cursor()

        # График для Мкр
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(NavigationToolbar(self.canvas, self))
        layout.addWidget(self.canvas)
        self.main.plotWidget.setLayout(layout)

        # График для вспомогательной кривой
        self.fhelp = plt.figure()
        self.chelp = FigureCanvas(self.fhelp)
        Vlayout_help = QVBoxLayout()
        Vlayout_help.addWidget(NavigationToolbar(self.chelp, self))
        Vlayout_help.addWidget(self.chelp)
        self.main.helpwidget.setLayout(Vlayout_help)

        # График для взлетной кривой
        self.fUp = plt.figure()
        self.cUp = FigureCanvas(self.fUp)
        Vlayout_Up = QVBoxLayout()
        Vlayout_Up.addWidget(NavigationToolbar(self.cUp, self))
        Vlayout_Up.addWidget(self.cUp)
        self.main.upwidget.setLayout(Vlayout_Up)

        # График для посадочной кривой
        self.fDown = plt.figure()
        self.cDown = FigureCanvas(self.fDown)
        Vlayout_Down = QVBoxLayout()
        Vlayout_Down.addWidget(NavigationToolbar(self.cDown, self))
        Vlayout_Down.addWidget(self.cDown)
        self.main.downwidget.setLayout(Vlayout_Down)

        # График для крейсерской кривой
        self.fCruise = plt.figure()
        self.cCruise = FigureCanvas(self.fCruise)
        Vlayout_Cruise = QVBoxLayout()
        Vlayout_Cruise.addWidget(NavigationToolbar(self.cCruise, self))
        Vlayout_Cruise.addWidget(self.cCruise)
        self.main.cruiswidget.setLayout(Vlayout_Cruise)

    def set(self):
        # Первая вкладка
        self.main.tabWidget_2.setTabVisible(0, False)
        self.main.tabWidget_2.setTabVisible(1, False)
        self.main.tabWidget_2.setTabVisible(2, False)
        self.main.tabWidget_2.setTabVisible(3, False)
        self.main.tabWidget_2.setTabVisible(4, False)
        self.main.tabWidget_2.setTabVisible(5, False)
        self.main.tabWidget_2.setTabVisible(6, False)

        self.main.buStart.clicked.connect(self.ButtonEnabled)
        self.main.buWing.clicked.connect(self.pressedWing)
        self.main.buFlapMulard.clicked.connect(self.pressedFlapMulard)
        self.main.buTail.clicked.connect(self.pressedTail)
        self.main.buPylon.clicked.connect(self.pressedPylon)
        self.main.buFuselage.clicked.connect(self.pressedFuselage)
        self.main.buGondola.clicked.connect(self.pressedGondola)
        self.main.buCommonData.clicked.connect(self.pressedCommonData)
        self.main.buShowAirPlan.clicked.connect(self.OpenPlan)
        self.main.buFlapChoose.clicked.connect(self.OpenFlapChoose)

        # вторая вкладка
        self.main.tabWidget.setTabVisible(0, False)
        self.main.tabWidget.setTabVisible(1, False)
        self.main.tabWidget.setTabVisible(2, False)
        self.main.tabWidget.setTabVisible(3, False)
        self.main.tabWidget.setTabVisible(4, False)

        # Построение вспомогательных кривых
        self.main.buMkr.clicked.connect(self.MakeMkr)
        self.main.buHelp.clicked.connect(self.MakeHelp)
        self.main.buUp.clicked.connect(self.MakeUp)
        self.main.buDown.clicked.connect(self.MakeDown)
        self.main.buCre.clicked.connect(self.MakeCruise)

        # Расчет переменных
        self.main.buCalWing.clicked.connect(self.CalculateWing)
        self.main.buCalFlapMulard.clicked.connect(self.CalculateFlapMulard)
        self.main.buCalTail.clicked.connect(self.CalculateTail)
        self.main.buCalPylon.clicked.connect(self.CalculatePylon)
        self.main.buCalFuselage.clicked.connect(self.CalculateFuselage)
        self.main.buCalGondola.clicked.connect(self.CalculateGondola)
        self.main.buCommonDataSafe.clicked.connect(self.SafeCommonData)

    def ButtonEnabled(self):
        self.pressedWing()
        self.main.buWing.setEnabled(True)
        self.main.buWing.setStyleSheet("background-color: #555555;")



    # ОПРЕДЕЛЕНИЕ ПЕРЕМЕННОЙ Кх ПО ГРАФИКУ
    def find_Kx(self, n, x_degree):
        list_x = [0, 10, 20, 30, 40, 50, 55]
        global Kx
        Kx = 0
        if n > 2:
            Kx = 1
            print('Kx = ' + str(Kx))
        else:
            if x_degree in list_x:
                Sql_request = 'SELECT Коэффициент FROM Коэф_Kx ' \
                              'WHERE Стреловидность = %s' % x_degree
                self.cursor.execute(Sql_request)
                Kx = float(self.cursor.fetchone()[0])
                print('Kx = ' + str(Kx))
            else:
                i = 0
                while Kx == 0:
                    if x_degree > list_x[i] and x_degree < list_x[i + 1]:
                        Sql_request = 'SELECT Коэффициент FROM Коэф_Kx ' \
                                      'WHERE Стреловидность = %s' % list_x[i]
                        self.cursor.execute(Sql_request)
                        x_1 = float(self.cursor.fetchone()[0])
                        Sql_request = 'SELECT Коэффициент FROM Коэф_Kx ' \
                                      'WHERE Стреловидность = %s' % list_x[i + 1]
                        self.cursor.execute(Sql_request)
                        x_2 = float(self.cursor.fetchone()[0])
                        middle = (x_1 + x_2) / 2
                        if x_degree % 10 == 5:
                            Kx = middle
                            print('Kx = ' + str(Kx))
                        else:
                            a = list_x[i] + 5
                            if x_degree < a:
                                Kx = (x_1 + middle) / 2
                                print('Kx = ' + str(Kx))
                            else:
                                Kx = (x_2 + middle) / 2
                                print('Kx = ' + str(Kx))
                    else:
                        i = i + 1

    # ОПРЕДЕЛЕНИЕ рН, аН ПО ТАБЛИЦЕ
    def find_with_H(self, H):
        global pH, aH
        pH = 0
        aH = 0
        h = float('%.1f' % (H / 1000))

        Sql_request = 'SELECT * FROM "Стандартная_атмосфера" ' \
                      'WHERE "Высота(км)" = %s' % str(h)
        self.cursor.execute(Sql_request)

        cor = self.cursor.fetchone()
        # print(cor)
        pHstr = cor[3]
        aHstr = cor[6]

        pH = float(pHstr)
        aH = float(aHstr)

        print('pH = ' + str(pH))
        print('aH = ' + str(aH))

    # ОПРЕДЕЛЕНИЕ Gm ПО ТАБЛИЦЕ
    def whatWeight(self, Gvzl):
        if Gvzl <= 20000:
            return '20000'
        if Gvzl <= 40000:
            return '40000'
        if Gvzl <= 80000:
            return '80000'
        if Gvzl <= 120000:
            return '120000'
        else:
            return '120001'

    def findGm(self):
        if type == 'ТРД':
            Sql_request = 'SELECT ТРД FROM "Полный запас топлива Gm" ' \
                          'WHERE "Gвзл, кг" = %s' % self.whatWeight(Gvzl)
            self.cursor.execute(Sql_request)
        elif type == 'ТВД и ПД':
            Sql_request = 'SELECT "ТВД и ПД" FROM "Полный запас топлива Gm" ' \
                          'WHERE "Gвзл, кг" = %s' % self.whatWeight(Gvzl)
            self.cursor.execute(Sql_request)

        return float('%.3f' % (float(self.cursor.fetchone()[0]) * 0.01 * Gvzl))

    # ОПРЕДЕЛЕНИЕ Kn ПО ГРАФИКУ
    def find_Kn(self, n):
        list_n = [1, 1.3, 1.5, 1.8, 2.7, 3]
        index = -1
        if n > 3:
            return -0.01 * n + 0.96
        else:
            if n in list_n:
                Sql_request = 'SELECT kn FROM Коэф_Kn ' \
                              'WHERE n = %s' % n
                self.cursor.execute(Sql_request)
                return float(self.cursor.fetchone()[0])
            else:
                i = 0
                while index == -1:
                    if n > list_n[i] and n < list_n[i + 1]:
                        index = i
                    else:
                        i = i + 1
                Sql_request = 'SELECT kn FROM Коэф_Kn ' \
                              'WHERE n = %s' % list_n[index]
                self.cursor.execute(Sql_request)
                first = float(self.cursor.fetchone()[0])
                Sql_request = 'SELECT kn FROM Коэф_Kn ' \
                              'WHERE n = %s' % list_n[index + 1]
                self.cursor.execute(Sql_request)
                second = float(self.cursor.fetchone()[0])
                return (first + second) / 2

    # ОПРЕДЕЛЕНИЕ Cya max профиля ПО ГРАФИКУ

    # ОПРЕДЕНИЕ КОЭФ Cyamax
    def ChooseCymaxprof(self, c_, Re):
        # Выборка
        list_c_ = [0.08, 0.1, 0.12, 0.14, 0.16, 0.18, 0.2]
        list_Re = [1, 2, 3, 4, 5, 6, 7, 8]
        if c_ in list_c_:
            if c_ == 0.08 and 3 <= Re <= 6:
                return 0.1 * Re + 0.8
            elif c_ == 0.1 and 0 <= Re <= 4:
                return 0.13 * Re + 0.85
            elif c_ == 0.12 and 0 <= Re <= 3:
                return 0.17 * Re + 0.83
            elif c_ == 0.14 and 0 <= Re <= 3:
                return 0.17 * Re + 0.83
            if Re in list_Re:
                Sql_request = 'SELECT Cyamaxprof FROM Коэф_Cyamaxprof ' \
                              'WHERE Re = %s AND Толщина= %s' % (Re, c_)
                self.cursor.execute(Sql_request)
                return float(self.cursor.fetchone()[0])
            elif Re > 8:
                Sql_request = 'SELECT Cyamaxprof FROM Коэф_Cyamaxprof ' \
                              'WHERE Re = %s AND Толщина= %s' % (8, c_)
                self.cursor.execute(Sql_request)
                return float(self.cursor.fetchone()[0])
            else:
                i = 0
                index = -1
                while index == -1:
                    if list_Re[i] < Re < list_Re[i + 1]:
                        index = i
                    else:
                        i = i + 1
                Sql_request = 'SELECT Cyamaxprof FROM Коэф_Cyamaxprof ' \
                              'WHERE Re = %s AND Толщина= %s' % (list_Re[index], c_)
                self.cursor.execute(Sql_request)
                first = float(self.cursor.fetchone()[0])
                # print(first)
                Sql_request = 'SELECT Cyamaxprof FROM Коэф_Cyamaxprof ' \
                              'WHERE Re = %s AND Толщина= %s' % (list_Re[index + 1], c_)
                self.cursor.execute(Sql_request)
                second = float(self.cursor.fetchone()[0])
                # print(second)
                return float('%.3f' % ((first + second) / 2))

    def find_Cyamaxprof(self):
        global Cyamaxprof, Re, Vmin
        v0 = 0.000014607  # коэф кинематической вязкости на высоте 0
        # определение числа Рейнольдса
        Vmin = 3.5 * math.sqrt(Gpol / S)
        Re_full = (Vmin * b) / v0
        Re = float('%.1f' % (Re_full / 10 ** 6))
        print('Re = ' + str(Re))
        print('c_ = ' + str(c_))

        # Вызов функции
        list_c_ = [0.08, 0.1, 0.12, 0.14, 0.16, 0.18, 0.2]
        if c_ in list_c_:
            Cyamaxprof = self.ChooseCymaxprof(c_, Re)
            print('Cyamaxprof = ' + str(Cyamaxprof))
        elif c_ < 0.08:
            Cyamaxprof = self.ChooseCymaxprof(0.08, Re)
        else:
            i = 0
            index = -1
            while index == -1:
                if list_c_[i] < c_ < list_c_[i + 1]:
                    index = i
                else:
                    i = i + 1
            first = self.ChooseCymaxprof(list_c_[index], Re)
            second = self.ChooseCymaxprof(list_c_[index + 1], Re)
            Cyamaxprof = float('%.3f' % ((first + second) / 2))
            print('Cyamaxprof = ' + str(Cyamaxprof))

    # ВЫЗОВ ФУНКЦИИ .ОПРЕДЕЛЕЛЕНИЯ ПРИРАЩЕНИЯ УГЛА. взависимости от относ хорды закрылков
    def call_da0(self, delta):
        list_bzak_ = [0.1, 0.2, 0.3]
        if bzak_ in list_bzak_:
            return (-1) * self.find_da0(bzak_, delta)
        elif bzak_ > 0.3:
            return (-1) * self.find_da0(0.3, delta)
        else:
            i = 0
            index = -1
            while index == -1:
                if list_bzak_[i] < bzak_ < list_bzak_[i + 1]:
                    index = i
                    first = self.find_da0(list_bzak_[index], delta)
                    second = self.find_da0(list_bzak_[index + 1], delta)
                    if (bzak_ * 100) % 10 == 5:
                        return (-1) * float('%.3f' % ((first + second) / 2))
                    elif (bzak_ * 100) % 10 < 5:
                        middle_a0_vzl = float('%.3f' % ((first + second) / 2))
                        return (-1) * float('%.3f' % ((first + middle_a0_vzl) / 2))
                    elif (bzak_ * 100) % 10 > 5:
                        middle_a0_vzl = float('%.3f' % ((first + second) / 2))
                        return (-1) * float('%.3f' % ((second + middle_a0_vzl) / 2))
                else:
                    i = i + 1

    # ОПРЕДЕЛЕНИЕ ПРИРАЩЕНИЯ УГЛА (взлетного и посадочного)
    def find_da0(self, bzak_, delta):
        list_b_ = [0.1, 0.2, 0.3]
        list_delta = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3]
        if bzak_ in list_b_:
            if bzak_ == 0.1 and 0 <= delta <= 0.6:
                return 0.158 * delta + 0.0022
            elif bzak_ == 0.2 and 0 <= delta <= 0.5:
                return 0.225 * delta + 0.0125
            elif delta in list_delta:
                Sql_request = 'SELECT delta_a0 FROM "Приращение взлетного угла" ' \
                              'WHERE b_zak = %s AND бvzl_pos= %s' % (bzak_, delta)
                self.cursor.execute(Sql_request)
                return float(self.cursor.fetchone()[0])
            elif delta > 1.3:
                Sql_request = 'SELECT delta_a0 FROM "Приращение взлетного угла" ' \
                              'WHERE b_zak = %s AND бvzl_pos= %s' % (bzak_, 1.3)
                self.cursor.execute(Sql_request)
                return float(self.cursor.fetchone()[0])
            else:
                i = 0
                index = -1
                while index == -1:
                    if list_delta[i] < delta < list_delta[i + 1]:
                        index = i
                    else:
                        i = i + 1
                Sql_request = 'SELECT delta_a0 FROM "Приращение взлетного угла" ' \
                              'WHERE b_zak = %s AND бvzl_pos= %s' % (bzak_, list_delta[index])
                self.cursor.execute(Sql_request)
                first = float(self.cursor.fetchone()[0])
                # print(first)
                Sql_request = 'SELECT delta_a0 FROM "Приращение взлетного угла" ' \
                              'WHERE b_zak = %s AND бvzl_pos= %s' % (bzak_, list_delta[index + 1])
                self.cursor.execute(Sql_request)
                second = float(self.cursor.fetchone()[0])
                # print(second)
                return float('%.3f' % ((first + second) / 2))

    # ОТКРЫТИЕ ВКЛАДОК ПО КНОПКАМ
    def pressedWing(self):
        self.main.tabWidget_2.setCurrentIndex(0)

    def pressedFlapMulard(self):
        self.main.tabWidget_2.setCurrentIndex(1)

    def pressedTail(self):
        self.main.tabWidget_2.setCurrentIndex(2)

    def pressedPylon(self):
        self.main.tabWidget_2.setCurrentIndex(3)

    def pressedFuselage(self):
        self.main.tabWidget_2.setCurrentIndex(4)

    def pressedGondola(self):
        self.main.tabWidget_2.setCurrentIndex(5)

    def pressedCommonData(self):
        self.main.tabWidget_2.setCurrentIndex(6)

    def OpenPlan(self):
        dlg = DialogPlan(self)
        dlg.show()

    def OpenFlapChoose(self):
        dialog = DialogMechanism(self)
        dialog.show()

    # РАСЧЕТ ИСХОДНЫХ ДАННЫХ КРЫЛА
    def CalculateWing(self):
        self.main.buFlapMulard.setEnabled(True)
        self.main.buFlapMulard.setStyleSheet("background-color: #555555;")

        # Хорда средняя
        global l, S, b
        l = float(self.main.ed_l.text().replace(',','.'))
        S = float(self.main.ed_S.text().replace(',','.'))
        b = float('%.3f' % (S / l))
        self.main.ed_b.setText(str(b))

        # Сужение
        global b0, bk, n
        b0 = float(self.main.ed_b0.text().replace(',','.'))
        bk = float(self.main.ed_bk.text().replace(',','.'))
        n = float('%.2f' % (b0 / bk))
        self.main.ed_n.setText(str(n))

        # Относительная толщина профиля
        global cmax, c_
        cmax = float(self.main.ed_cmax.text().replace(',','.'))
        c_ = float('%.2f' % (cmax / b))
        self.main.ed_c_.setText(str(c_))

        # Относительная координата максимальной толщины
        global xc, xc_
        xc = float(self.main.ed_xc.text().replace(',','.'))
        xc_ = float('%.3f' % (xc / b))
        self.main.ed_xc_.setText(str(xc_))

        # Относительная кривизна профиля
        global fmax, f_
        fmax = float(self.main.ed_fmax.text().replace(',','.'))
        f_ = float('%.3f' % (100 * fmax / b))
        self.main.ed_f_.setText(str(f_))

        # Угол атаки нулевой подъемной силы
        global a0
        expression = (-1) * 0.9 * f_
        a0 = float('%.3f' % expression)
        self.main.ed_a0.setText(str(a0))

        # Относительная координата фокуса профиля
        global xf, xf_
        xf = float(self.main.ed_xf.text().replace(',','.'))
        xf_ = float('%.3f' % (xf / b))
        self.main.ed_xf_.setText(str(xf_))

        # Удлинение геометрическое
        global lamda
        lamda = float('%.3f' % (l ** 2 / S))
        self.main.ed_lamda.setText(str(lamda))

        # Относительная площадь, занятая фюзеляжем
        global Sf, Sf_
        Sf = float(self.main.ed_Sf.text().replace(',','.'))
        Sf_ = float('%.3f' % (Sf / S))
        self.main.ed_Sf_.setText(str(Sf_))

        # Относительная площадь, занятая гондолами двигателей
        global Sgd, Sgd_
        Sgd = float(self.main.ed_Sgd.text().replace(',','.'))
        Sgd_ = float('%.3f' % (Sgd / S))
        self.main.ed_Sgd_.setText(str(Sgd_))

        # Относительная площадь, занятая гондолами шасси
        global Sgsh, Sgsh_
        Sgsh = float(self.main.ed_Sgsh.text().replace(',','.'))
        Sgsh_ = float('%.3f' % (Sgsh / S))
        self.main.ed_Sgsh_.setText(str(Sgsh_))

        # Относительная площадь, не обтекаемая потоком
        global S_
        S_ = round(Sf_ + Sgd_ + Sgsh_, 3)
        self.main.ed_S_.setText(str(S_))

        # Удлинение эффективное
        global lamdaef, Kx, x_degree
        x_degree = float(self.main.ed_x_deg.text().replace(',','.'))
        self.find_Kx(n, x_degree)
        expression = (lamda * Kx) / (1 + S_)
        lamdaef = float('%.3f' % expression)
        self.main.ed_lamdaef.setText(str(lamdaef))

        # Производная коэф подъемной силы по углу атаки
        global caya, xc_degree
        xc_degree = float(self.main.ed_xc_deg.text().replace(',','.')) * math.pi / 180
        expression = (2 * math.pi * lamdaef * math.cos(xc_degree)) / (57.3 * (lamdaef + 2 * math.cos(xc_degree)))
        caya = float('%.3f' % expression)
        self.main.ed_caya.setText(str(caya))

        # Относительная площадь, обдуваемая винтами
        global Sobd, Sobd_
        Sobd = float(self.main.ed_Sobd.text().replace(',','.'))
        Sobd_ = float('%.3f' % (Sobd / S))
        self.main.ed_Sobd_.setText(str(Sobd_))

        # Относительная координата точки перехода ЛПС в ТПС
        global xtau_
        expression = xc_ * (1 - Sobd_)
        xtau_ = float('%.3f' % expression)
        self.main.ed_xtau_.setText(
            str(xtau_))  # У РЕБЯТ РАВНО 0 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        # Коэффициент момента профиля
        global cmo
        cmo = float('%.3f' % ((-1) * 0.005 * math.pi * f_))
        self.main.ed_cmo.setText(str(cmo))

        # Определение переменных
        global h
        h = float(self.main.ed_h.text().replace(',','.'))

    # РАСЧЕТ ЗАКРЫЛОК И ПРЕДКРЫЛОК
    def CalculateFlapMulard(self):
        self.main.buTail.setEnabled(True)
        self.main.buTail.setStyleSheet("background-color: #555555;")

        # Определение переменных
        global xshzak
        xshzak = float(self.main.ed_xshzak.text().replace(',','.'))

        # Относительная хорда закрылки
        global bzak, bzak_
        bzak = float(self.main.ed_bzak.text().replace(',','.'))
        bzak_ = float('%.2f' % (bzak / b))
        self.main.ed_bzak_.setText(str(bzak_))

        # Относ площадь крыла, обслуживаемая закрылками
        global Sobzak, Sobzak_
        Sobzak = float(self.main.ed_Sobzak.text().replace(',','.'))
        Sobzak_ = float('%.3f' % (Sobzak / S))
        self.main.ed_Sobzak_.setText(str(Sobzak_))

        # Хорда средняя крыла с выпущенными закрылком
        global bsrzak, lzak
        lzak = float(self.main.ed_lzak.text().replace(',','.'))
        bsrzak = float('%.3f' % (Sobzak / lzak))
        self.main.ed_bsrzak.setText(str(bsrzak))

        # Расстояние от края закрылка до земли при взлете
        global deltavzl, hvzl
        deltavzl = float(self.main.ed_deltavzl.text().replace(',','.')) * math.pi / 180
        hvzl = float('%.3f' % (h - math.sin(deltavzl) * bzak))  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.main.ed_hvzl.setText(str(hvzl))

        # Расстояние от края закрылка до земли при посадке
        global deltapos, hpos
        deltapos = float(self.main.ed_deltapos.text().replace(',','.')) * math.pi / 180
        hpos = float('%.3f' % (h - math.sin(deltapos) * bzak))  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.main.ed_hpos.setText(str(hpos))

        # Относ площадь крыла, обслуживаемая предкрылком
        global Sobpr, Sobpr_
        Sobpr = float(self.main.ed_Sobpr.text().replace(',','.'))
        Sobpr_ = float('%.3f' % (Sobpr / S))
        self.main.ed_Sobpr_.setText(str(Sobpr_))

    # РАСЧЕТ ГОРИЗОНТ И ВЕРТИКАЛ ОПЕРЕНИЯ
    def CalculateTail(self):
        self.main.buPylon.setEnabled(True)
        self.main.buPylon.setStyleSheet("background-color: #555555;")

        # Определение переменных
        global bgo, xgo, bv, Sv, bvo, lvo, Svo
        bgo = float(self.main.ed_bgo.text().replace(',','.'))
        xgo = float(self.main.ed_xgo.text().replace(',','.'))
        bv = float(self.main.ed_bv.text().replace(',','.'))
        Sv = float(self.main.ed_Sv.text().replace(',','.'))
        bvo = float(self.main.ed_bvo.text().replace(',','.'))
        lvo = float(self.main.ed_lvo.text().replace(',','.'))
        Svo = float(self.main.ed_Svo.text().replace(',','.'))

        # Относительная толщина горизонт и вертикал оперения
        global cgo_, cvo_
        cvo_ = cgo_ = c_ - 0.02
        self.main.ed_cgo_.setText(str(cgo_))
        self.main.ed_cvo_.setText(str(cvo_))

        # Удлинение гор оперения
        global lgo, Sgo, lamdago
        lgo = float(self.main.ed_lgo.text().replace(',','.'))
        Sgo = float(self.main.ed_Sgo.text().replace(',','.'))
        lamdago = float('%.3f' % (lgo ** 2 / Sgo))
        self.main.ed_lamdago.setText(str(lamdago))

    # ОПРЕДЕЛЕНИЕ ПЕРЕМЕННЫХ ПИЛОНА
    def CalculatePylon(self):
        self.main.buFuselage.setEnabled(True)
        self.main.buFuselage.setStyleSheet("background-color: #555555;")

        global bp, cp_, Sp
        bp = float(self.main.ed_bp.text().replace(',','.'))
        cp_ = float(self.main.ed_cp_.text().replace(',','.'))
        Sp = float(self.main.ed_Sp.text().replace(',','.'))

    # РАСЧЕТ ДАННЫХ ФЮЗЕЛЯЖА
    def CalculateFuselage(self):
        self.main.buGondola.setEnabled(True)
        self.main.buGondola.setStyleSheet("background-color: #555555;")

        # Диаметр миделя
        global Df, Smf
        Smf = float(self.main.ed_Smf.text().replace(',','.'))
        Df = float('%.3f' % (math.sqrt(4 * Smf / math.pi)))
        self.main.ed_Df.setText(str(Df))

        # Удлинение
        global lamdaf, lf
        lf = float(self.main.ed_lf.text().replace(',','.'))
        lamdaf = float('%.3f' % (lf / Df))
        self.main.ed_lamdaf.setText(str(lamdaf))

        # Смоченная поверхность
        global Ssm
        Ssm = float('%.3f' % (2.5 * lf * Df))
        self.main.ed_Ssm.setText(str(Ssm))

        # Удлинение носовой части
        global lnf, lamdanf
        lnf = float(self.main.ed_lnf.text().replace(',','.'))
        lamdanf = float('%.3f' % (lnf / Df))
        self.main.ed_lamdanf.setText(str(lamdanf))

    # РАСЧЕТ ДАННЫХ ГОНДОЛ ДВИГАТЕЛЯ И ШАССИ
    def CalculateGondola(self):

        # Удлинение гондола двигателя
        global lgd, Dgd, lamdagd
        lgd = float(self.main.ed_lgd.text().replace(',','.'))
        Dgd = float(self.main.ed_Dgd.text().replace(',','.'))
        lamdagd = float('%.3f' % (lgd / Dgd))
        self.main.ed_lamdagd.setText(str(lamdagd))

        # Удлинение смоченная поверхность гондола двигателя
        global Ssm_gd
        Ssm_gd = float('%.3f' % (2.5 * lgd * Dgd))
        self.main.ed_Ssmgd.setText(str(Ssm_gd))

        # Удлинение удлинение носовой части гондола двигателя
        global ln_gd, lamdan_gd
        ln_gd = float(self.main.ed_lngd.text().replace(',','.'))
        lamdan_gd = float('%.3f' % (ln_gd / Dgd))
        self.main.ed_lamdangd.setText(str(lamdan_gd))

        # Удлинение гондола шасси
        global lgsh, Dgsh, lamdagsh
        lgsh = float(self.main.ed_lgsh.text().replace(',','.'))
        Dgsh = float(self.main.ed_Dgsh.text().replace(',','.'))
        lamdagsh = float('%.3f' % (lgsh / Dgsh))
        self.main.ed_lamdagsh.setText(str(lamdagsh))

        # Удлинение смоченная поверхность гондола шасси
        global Ssm_gsh
        Ssm_gsh = float('%.3f' % (2.5 * lgsh * Dgsh))
        self.main.ed_Ssmgsh.setText(str(Ssm_gsh))

        # Удлинение удлинение носовой части гондола шасси
        global ln_gsh, lamdan_gsh
        ln_gsh = float(self.main.ed_lngsh.text().replace(',','.'))
        lamdan_gsh = float('%.3f' % (ln_gsh / Dgsh))
        self.main.ed_lamdangsh.setText(str(lamdan_gsh))

    # СОХРАНЕНИЕ ОБЩИХ ДАННЫХ
    def SafeCommonData(self):
        self.main.buMkr.setEnabled(True)
        self.main.buMkr.setStyleSheet("background-color: #555555;")

        global Gvzl, V, number, P0, H, Dv, Fv
        Dv = float(self.main.ed_Dv.text().replace(',','.'))
        Fv = float('%.3f' % (math.pi * Dv * Dv / 4))
        Gvzl = float(self.main.ed_Gvzl.text().replace(',','.'))
        V = float(self.main.ed_V.text())
        number = float(self.main.ed_number.text().replace(',','.'))
        P0 = float(self.main.ed_P0.text().replace(',','.'))
        H = float(self.main.ed_H.text().replace(',','.'))
        self.find_with_H(H)

        # Тип двигателей
        global type
        if self.main.radioButton_PD.isChecked():
            type = 'ТВД и ПД'
        elif self.main.radioButton_TRD.isChecked():
            type = 'ТРД'
        # ELSE ERROR

        if type != '':
            global Gm
            Gm = self.findGm()

    # РАСЧЕТ И ПОСТРОЕНИЕ КРИВОЙ ЗАВИСИМОСТИ Мкр
    def MakeMkr(self):
        self.main.tabWidget.setCurrentIndex(0)
        self.main.buHelp.setEnabled(True)
        self.main.buHelp.setStyleSheet("background-color: #555555; height: 30px;")

        # Расчет координат вспомогательной прямой
        arr_cya = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
        arr_Mkr = []
        for cya in arr_cya:
            expression = 1 - 0.445 * math.pow(lamdaef - 1, 1 / 9) * (0.175 + 3.25 * c_) * (
                    math.cos(x_degree * math.pi / 180) + (0.365 * cya ** 2) / math.cos(
                x_degree * math.pi / 180) ** 5)
            arr_Mkr.append(float('%.3f' % expression))

        # Занесение координат в БД
        arr = []
        arr_ = [0, 1]
        for i in range(8):
            arr_[0] = arr_cya[i]
            arr_[1] = arr_Mkr[i]
            arr.append(tuple(arr_))
        cor = tuple(arr)
        self.cursor.execute('DELETE FROM "Кривая зависимость Мкр";', )
        sqlite_insert_query = """INSERT INTO 'Кривая зависимость Мкр'
                                         (Cya, Мкр) VALUES (?, ?);"""
        self.cursor.executemany(sqlite_insert_query, cor)
        self.connection.commit()

        # Отображение в приложении
        SQLquery = 'SELECT * FROM "Кривая зависимость Мкр"'

        # tablerow = 0
        # self.main.tableWidget_Mkr.setRowCount(8)
        # self.main.tableWidget_Mkr.setColumnCount(2)
        # for row in self.cursor.execute(SQLquery):
        #     for col in range(2):
        #         item = QtWidgets.QTableWidgetItem(str(row[col]))
        #         item.setTextAlignment(QtCore.Qt.AlignCenter)
        #         item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        #         self.main.tableWidget_Mkr.setItem(tablerow, col, item)
        #     tablerow = tablerow + 1

        tablecol = 1
        self.main.tableWidget_Mkr.setRowCount(2)
        self.main.tableWidget_Mkr.setColumnCount(9)
        for row in self.cursor.execute(SQLquery):
            for col in range(2):
                item = QtWidgets.QTableWidgetItem(str(row[col]))
                tablerow = col
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.main.tableWidget_Mkr.setItem(tablerow, tablecol, item)
            tablecol = tablecol + 1

        item1 = QtWidgets.QTableWidgetItem('Cya')
        item2 = QtWidgets.QTableWidgetItem('Мкр')
        self.main.tableWidget_Mkr.setItem(0, 0, item1)
        self.main.tableWidget_Mkr.setItem(1, 0, item2)

        # Расчет точки ?????
        global Gpol, Mrasch
        Vms = float('%.3f' % (V / 3.6))  # км/ч в м/с
        Mrasch = float('%.4f' % (Vms / aH))  # определение расчетного числа маха
        Gpol = Gvzl - 0.5 * Gm
        cya_rasch = float('%.4f' % ((2 * Gpol * g) / (pH * Vms * Vms * S)))

        # Отображение найденных переменных
        self.main.la_Mrasch_Mkr.setText(str(Mrasch))
        self.main.la_Gpol_Mkr.setText(str(Gpol))
        self.main.la_Cyarasch_Mkr.setText(str(cya_rasch))

        # Отрисовка
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        # plot data
        ax.plot(arr_cya, arr_Mkr, color='k', label='Мкр = f(cya)')
        ax.plot(cya_rasch, Mrasch, marker='.', color='navy', label='')

        ax.text(cya_rasch, Mrasch, '  A(Мрасч;Суа расч)', rotation=0, fontsize=7)
        ax.legend(loc='lower left')
        ax.set_title('Кривая зависимости Мкр = f(cya)', loc='right', pad=5, fontsize=11)



        # ax.set_xlabel('Суа')
        # ax.set_ylabel('Мкр')
        # ax.vlines(cya_rasch, arr_Mkr[7], Mrasch, color='lightgray',linewidth=1,linestyle='--')
        # ax.grid()
        self.canvas.draw()

    # ПОСТРОЕНИЕ ВСПОМОГАТЕЛЬНОЙ КРИВОЙ cya = f(a)
    def MakeHelp(self):
        self.main.buUp.setEnabled(True)
        self.main.buUp.setStyleSheet("background-color: #555555; height: 30px;")

        self.main.tabWidget.setCurrentIndex(1)
        self.fhelp.clear()
        ax = self.fhelp.add_subplot(111)

        # Линейный участок, характеризующий безотрывное обтекания крыла
        # Точка 1 - (а0, 0)

        # Точка 2 - (а, суа)
        alfa_px2 = 5  # произвольно
        cya_py2 = float('%.3f' % (caya * (alfa_px2 - a0)))

        # Точка 4 - (а, суа_max)
        # Коэф cya max
        global Kn, Cyamax
        Kn = float('%.3f' % self.find_Kn(n))
        print('Kn = ' + str(Kn))
        self.find_Cyamaxprof()
        Cyamax = float('%.3f' % (Cyamaxprof * Kn * (1 + math.cos(x_degree * math.pi / 180)) / 2))
        print('Cyamax = ' + str(Cyamax))
        k = cya_py2 / (alfa_px2 - a0)
        b = (-1) * k * a0
        px4 = float('%.3f' % ((Cyamax - b) / k))

        # Точка 3 - (x, 0.85 * суа_max)
        cya_py3 = float('%.3f' % (0.85 * Cyamax))
        px3 = float('%.3f' % ((cya_py3 - b) / k))

        # Точка 5 - (deltaalfa ,суа_max)
        deltaalfa = 2  # !!! произвольно
        px5 = px4 + deltaalfa
        py5 = Cyamax

        # Отображение найденных переменных
        self.main.la_1_help.setText('(' + str(a0) + '; ' + str(0) + ')')
        self.main.la_2_help.setText('(' + str(alfa_px2) + '; ' + str(cya_py2) + ')')
        self.main.la_3_help.setText('(' + str(px3) + '; ' + str(cya_py3) + ')')
        self.main.la_4_help.setText('(' + str(px4) + '; ' + str(Cyamax) + ')')
        self.main.la_5_help.setText('(' + str(px5) + '; ' + str(Cyamax) + ')')

        self.main.la_Re_help.setText(str(Re))
        self.main.la_Vmin_help.setText(str(float('%.3f' % Vmin)))
        self.main.la_Cyamaxprof_help.setText(str(Cyamaxprof))
        self.main.la_Kn_help.setText(str(Kn))

        # Отрисовка
        arrX_ = [a0, alfa_px2, px3, px4]
        arrY_ = [0, cya_py2, cya_py3, Cyamax]
        ax.plot(arrX_, arrY_, '--', label='Cya=f(a)_', color='k')
        arrX = [a0, alfa_px2, px3]
        arrY = [0, cya_py2, cya_py3]
        ax.plot(arrX, arrY, label='Cya=f(a)', color='k')

        ax.plot(a0, 0, marker='.')
        ax.plot(alfa_px2, cya_py2, marker='.')
        ax.plot(px3, cya_py3, marker='.')
        ax.plot(px4, Cyamax, marker='.')
        ax.plot(px5, py5, marker='.')

        # x=np.array( [px3,px5])
        # y = np.array([cya_py3, Cyamax])
        # x_new = np.linspace(x.min(), x.max(), 500)
        # f = interpolate.interp1d(x, y, kind='quadratic')
        # y_smooth = f(x_new)
        # ax.plot(x_new, y_smooth)

        ax.set_title('Вспомогательная кривая Cya = f(a)', loc='right', pad=5, fontsize=11)
        ax.legend(loc='lower right')
        # arc = matplotlib.patches.Arc((px5, cya_py3), deltaalfa*2, (Cyamax-cya_py3)*2, 180, 270)

        # ax.add_patch(arc)
        self.chelp.draw()

    # ПОСТРОЕНИЕ ВЗЛЕТНОЙ КРИВОЙ (С УЧЕТОМ И БЕЗ УЧЕТА ВЛИЯНИЯ ЭКРАНА ЗЕМЛИ)
    def MakeUp(self):
        self.main.tabWidget.setCurrentIndex(2)
        self.main.buDown.setEnabled(True)
        self.main.buDown.setStyleSheet("background-color: #555555; height: 30px;")

        # 1) Без учета влияния экрана земли

        # Определение переменных по графикам и таблицам (dCyamax и da0_vzl)
        global da0_vzl, dCyamax
        Sql_request = 'SELECT deltaCyamax FROM Закрылки WHERE Тип_механизации = %s' % '"' + Flap_type + '"'
        self.cursor.execute(Sql_request)
        dCyamax = float(self.cursor.fetchone()[0])  # ВЗЯТЬ ВСЕ СТОЛБЦЫ С БД
        da0_vzl = self.call_da0(deltavzl)  # определение приращения угла атаки нулевой подъемной силы в радианах

        # Преращение коэф подъем силы от выпуска предкрылков
        dCyamax_pr = 0.6 * Sobpr_

        # Преращение коэф подъем силы от выпуска закрылков
        # Sobzak_ = 0.459
        # da0_vzl = -0.16

        dCyamax_zak_vzl = float('%.3f' % (
                4.83 * dCyamax * Sobzak_ * abs(da0_vzl) * math.cos(xshzak * math.pi / 180) * math.cos(
            xshzak * math.pi / 180)))

        # УРАВНЕНИЯ ПРИ НАЛИЧИИ ВИНТОВ

        # Максимальный коэф подъемной силы при взлете
        Cyamax_vzl = float('%.3f' % (Cyamax + dCyamax_pr + dCyamax_zak_vzl))  # +dCya_obd
        a0_vzl = float('%.3f' % (a0 + da0_vzl * 180 / math.pi))  # +da0_obd

        # Точка
        cya = float('%.3f' % (caya * (5 - a0_vzl)))
        k = cya / (5 - a0_vzl)
        b = (-1) * k * a0_vzl
        px3 = float('%.3f' % ((Cyamax_vzl - b) / k))

        # Отображение найденных переменных
        self.main.la_dCyamaxpr_Up.setText(str(dCyamax_pr))
        self.main.la_dCyamaxzakvzl_Up.setText(str(dCyamax_zak_vzl))
        self.main.la_dCyaobd_Up.setText(str(0))  # найти переменную с винтами
        self.main.la_Cyamax_Up.setText(str(Cyamax))
        self.main.la_Cyamaxvzl_Up.setText(str(Cyamax_vzl))
        self.main.la_dCyamax_Up.setText(str(dCyamax))
        self.main.la_da0vzl_Up.setText(str(da0_vzl))
        self.main.la_da0obd_Up.setText(str(0))  # найти переменную с винтами
        self.main.la_a0_Up.setText(str(a0))
        self.main.la_a0vzl_Up.setText(str(a0_vzl))
        self.main.la_Cya_Up.setText(str(cya))

        # Отрисовка
        self.fUp.clear()
        ax = self.fUp.add_subplot(111)

        points_a = [a0_vzl, 5]
        points_Cya = [0, cya]
        ax.plot(points_a, points_Cya, marker='.', color='k')
        ax.plot(px3, Cyamax_vzl, marker='.', color='k')

        # 2) С учетом влияния экрана земли

        # Приращение КПС, вызванный экранным влиянияем земли
        dCyamax_zak_vzl_scrin = float('%.3f' % (-1 * 0.115 * math.exp(-0.5 * h / bsrzak) * Cyamax_vzl))

        # КПС, вызванный экранным влиянияем земли
        Cyamax_vzl_scrin = float('%.3f' % (Cyamax_vzl + dCyamax_zak_vzl_scrin))

        # Фиктивное удлинение крыла, учитывающее влияние экрана земли
        lamdaef_scrin = float('%.3f' % ((lamdaef / 2.23) * ((math.pi * l) / (8 * hvzl) + 2)))

        # Производная с учетом влияния экрана земли
        expression = (2 * math.pi * lamdaef_scrin * math.cos(x_degree * math.pi / 180)) / (
                57.3 * (lamdaef_scrin + 2 * math.cos(x_degree * math.pi / 180)))
        caya_scrin = float('%.3f' % expression)

        # Точка
        cya = float('%.3f' % (caya_scrin * (5 - a0_vzl)))
        k = cya / (5 - a0_vzl)
        b = (-1) * k * a0_vzl
        px3 = float('%.3f' % ((Cyamax_vzl_scrin - b) / k))

        # Отображение найденных переменных
        self.main.la_dCyamaxvzl_scrin_Up.setText(str(dCyamax_zak_vzl_scrin))
        self.main.la_Cyamaxvzl_scrin_Up.setText(str(Cyamax_vzl_scrin))
        self.main.la_Caya_scrin_Up.setText(str(caya_scrin))
        self.main.la_lamda_scrin_Up.setText(str(lamdaef_scrin))
        self.main.la_Cya_scrin_Up.setText(str(cya))

        # Отрисовка
        points_Cya[1] = cya
        ax.plot(points_a, points_Cya, marker='.', color='k')
        ax.plot(px3, Cyamax_vzl_scrin, marker='.')

    # ПОСТРОЕНИЕ ПОСАДОЧНЫХ КРИВЫХ (С УЧЕТОМ И БЕЗ УЧЕТА ВЛИЯНИЯ ЭКРАНА ЗЕМЛИ)
    def MakeDown(self):
        self.main.tabWidget.setCurrentIndex(3)
        self.main.buCre.setEnabled(True)
        self.main.buCre.setStyleSheet("background-color: #555555; height: 30px;")

        # 1) Без учета влияния экрана земли

        #    Определение переменных
        da0_pos = self.call_da0(deltapos)
        dCyamax_pr = 0.6 * Sobpr_  # преращение коэф подъем силы от выпуска предкрылков

        # Приращение КПС при выпущенных закрылках при посадке
        # da0_pos = -0.195
        # Sobzak_ = 0.459
        dCya_max_zak_pos = float(
            '%.3f' % (4.83 * dCyamax * Sobzak_ * abs(da0_pos) * (math.cos(xshzak * math.pi / 180) ** 2)))

        # КПС при посадке
        Cya_max_pos = float('%.3f' % (Cyamax + dCyamax_pr + dCya_max_zak_pos))
        a0_pos = float('%.3f' % (a0 + da0_pos * 180 / math.pi))

        # Точка
        cya =float('%.3f' % (caya * (5 - a0_pos)))
        k = cya / (5 - a0_pos)
        b = -1 * k * a0_pos
        alfa_point = float('%.3f' % ((Cya_max_pos - b) / k))

        # Отображение найденных переменных
        self.main.la_dCyamaxpr_Down.setText(str(dCyamax_pr))
        self.main.la_dCyamaxzakpos_Down.setText(str(dCya_max_zak_pos))
        self.main.la_Cyamax_Down.setText(str(Cyamax))
        self.main.la_Cyamaxpos_Down.setText(str(Cya_max_pos))
        self.main.la_dCyamax_Down.setText(str(dCyamax))
        self.main.la_da0pos_Down.setText(str(da0_pos))
        self.main.la_a0_Down.setText(str(a0))
        self.main.la_a0pos_Down.setText(str(a0_pos))
        self.main.la_Cya_Down.setText(str(cya))

        # Отрисовка
        self.fDown.clear()  # отчистка графика
        ax = self.fDown.add_subplot(111)
        points_a=[a0_pos, 5]
        points_cya=[0, cya]
        ax.plot(points_a, points_cya, marker='.', color='k')
        ax.plot(alfa_point, Cya_max_pos, marker='.', color='k')

        # 2) C учетом влияния экрана земли

        #    определение переменных
        x = x_degree * math.pi / 180
        h_pos = hpos / bsrzak

        # определение производной caya
        lamda_scrin = float('%.3f' % ((lamdaef / 2.23) * ((math.pi * l) / (8 * hpos) + 2)))
        caya_scrin = float(
            '%.3f' % ((2 * math.pi * lamda_scrin * math.cos(x)) / (57.3 * (lamda_scrin + 2 * math.cos(x)))))

        # макс КПС силы при посадке с учетом экрана земли с выпущенными закрылками
        dCya_max_zak_pos_scrin = float('%.3f' % (-0.115 * math.exp(-0.5 * h_pos) * Cya_max_pos))

        # макс КПС силы при посадке с учетом экрана земли
        Cya_max_pos_scrin = float('%.3f' % (Cya_max_pos + dCya_max_zak_pos_scrin))

        #   Точка
        cya_scrin = float('%.3f' % (caya_scrin * (5 - a0_pos)))
        k = cya_scrin / (5 - a0_pos)
        b = -1 * k * a0_pos
        alfa_point_scrin = float('%.3f' % ((Cya_max_pos_scrin - b) / k))

        # Отображение найденных переменных
        self.main.la_dCyamaxpos_scrin_Down.setText(str(dCya_max_zak_pos_scrin))
        self.main.la_Cyamaxpos_scrin_Down.setText(str(Cya_max_pos_scrin))
        self.main.la_Caya_scrin_Down.setText(str(caya_scrin))
        self.main.la_lamda_scrin_Down.setText(str(lamda_scrin))
        self.main.la_Cya_scrin_Down.setText(str(cya_scrin))

        # Отрисовка
        points_cya[1]=cya_scrin
        ax.plot(points_a, points_cya, '--', marker='.', color='r')
        ax.plot(alfa_point_scrin, Cya_max_pos_scrin, marker='.', color='r')


    # Выбор чисел Маха от типа двигателя
    def func_type(self, type):
        if type == 'ТРД':
            list_M = [float('%.3f' % Mrasch), 0, 0.7, 0.8, 0.85, 0.9, 0.95]
            return list_M
        elif type == 'ТВД и ПД':
            list_M = [float('%.3f' % Mrasch), 0, 0.4, 0.5, 0.6, 0.7]
            return list_M

    # ПОСТРОЕНИЕ КРЕЙСЕРСКИХ КРИВЫХ
    def MakeCruise(self):
        self.main.tabWidget.setCurrentIndex(4)

        list_M = self.func_type(type)
        list_caya_szh = []
        list_cya = []
        for M in list_M:
            caya_szh = caya / math.sqrt(1 - M ** 2)
            list_caya_szh.append(float('%.3f' % caya_szh))

            cya = caya_szh * (5 - a0)
            list_cya.append(float('%.3f' % cya))

        #     Построение
        self.fCruise.clear()
        ax = self.fCruise.add_subplot(111)
        for cya in list_cya:
            point_alfa = [a0, 5]
            point_cya = [0, cya]
            ax.plot(point_alfa, point_cya, color='k')
            ax.text(5.01, cya, 'M = ' + str(list_M[list_cya.index(cya)]), rotation=0, fontsize=7)

        ax.vlines(5, 0, list_cya[-1], color='k', linewidth=1, linestyle='--')
        ax.set_title('Крейсерские кривые Суа = f(a)', loc='right', pad=5, fontsize=11)

        # Занесение координат в БД
        arr = []
        arr_ = [0, 1, 2]
        for i in range(len(list_M)):
            arr_[0] = list_M[i]
            arr_[1] = list_caya_szh[i]
            arr_[2] = list_cya[i]
            arr.append(tuple(arr_))
        cor = tuple(arr)
        self.cursor.execute('DELETE FROM "Крейсерская кривая";', )
        sqlite_insert_query = """INSERT INTO 'Крейсерская кривая'
                                                (M, Caya_szh, Cya) VALUES (?, ?, ?);"""
        self.cursor.executemany(sqlite_insert_query, cor)
        self.connection.commit()

        # Отображение в таблице
        SQLquery = 'SELECT * FROM "Крейсерская кривая"'

        tablecol = 1
        self.main.tableWidget_Cruise.setRowCount(3)
        self.main.tableWidget_Cruise.setColumnCount(len(list_M) + 1)
        for row in self.cursor.execute(SQLquery):
            for col in range(3):
                item = QtWidgets.QTableWidgetItem(str(row[col]))
                tablerow = col
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.main.tableWidget_Cruise.setItem(tablerow, tablecol, item)
            tablecol = tablecol + 1

        item1 = QtWidgets.QTableWidgetItem('М')
        item2 = QtWidgets.QTableWidgetItem('Суа сж')
        item3 = QtWidgets.QTableWidgetItem('Суа')
        self.main.tableWidget_Cruise.setItem(0, 0, item1)
        self.main.tableWidget_Cruise.setItem(1, 0, item2)
        self.main.tableWidget_Cruise.setItem(2, 0, item3)


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    # window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение
