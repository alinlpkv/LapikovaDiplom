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

# CONST
g = 9.8

# ВЫСЧИТАННЫЕ
Gpol = 0 # полетный вес самолета
Cyamax = 0


class ExampleApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.main = Ui_MainWindow()
        self.main.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.show()
        self.set()
        self.connection = sqlite3.connect('bd.db')
        self.cursor = self.connection.cursor()

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(NavigationToolbar(self.canvas, self))
        layout.addWidget(self.canvas)
        self.main.plotWidget.setLayout(layout)

        self.fhelp = plt.figure()
        self.chelp = FigureCanvas(self.fhelp)
        Vlayout_help = QVBoxLayout()
        Vlayout_help.addWidget(NavigationToolbar(self.chelp, self))
        Vlayout_help.addWidget(self.chelp)
        self.main.helpwidget.setLayout(Vlayout_help)

        self.fUp = plt.figure()
        self.cUp = FigureCanvas(self.fUp)
        Vlayout_Up = QVBoxLayout()
        Vlayout_Up.addWidget(NavigationToolbar(self.cUp, self))
        Vlayout_Up.addWidget(self.cUp)
        self.main.upwidget.setLayout(Vlayout_Up)


    def set(self):
        # Первая вкладка
        self.main.tabWidget_2.setTabVisible(0, False)
        self.main.tabWidget_2.setTabVisible(1, False)
        self.main.tabWidget_2.setTabVisible(2, False)
        self.main.tabWidget_2.setTabVisible(3, False)
        self.main.tabWidget_2.setTabVisible(4, False)
        self.main.tabWidget_2.setTabVisible(5, False)
        self.main.tabWidget_2.setTabVisible(6, False)
        self.main.tabWidget_2.setTabVisible(7, False)
        self.main.buWing.clicked.connect(self.pressedWing)
        self.main.buFlapMulard.clicked.connect(self.pressedFlapMulard)
        self.main.buTail.clicked.connect(self.pressedTail)
        self.main.buPylon.clicked.connect(self.pressedPylon)
        self.main.buFuselage.clicked.connect(self.pressedFuselage)
        self.main.buGondola.clicked.connect(self.pressedGondola)
        self.main.buCommonData.clicked.connect(self.pressedCommonData)
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

        # Расчет переменных
        self.main.buCalWing.clicked.connect(self.CalculateWing)
        self.main.buCalFlapMulard.clicked.connect(self.CalculateFlapMulard)
        self.main.buCalTail.clicked.connect(self.CalculateTail)
        self.main.buCalPylon.clicked.connect(self.CalculatePylon)
        self.main.buCalFuselage.clicked.connect(self.CalculateFuselage)
        self.main.buCalGondola.clicked.connect(self.CalculateGondola)
        self.main.buCommonDataSafe.clicked.connect(self.SafeCommonData)

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

        print('pH = '+str(pH))
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
        global Kn
        Kn = 0
        index = 0
        if n > 3:
            Kn = -0.01 * n + 0.96
        else:
            if n in list_n:
                Sql_request = 'SELECT kn FROM Коэф_Kn ' \
                              'WHERE n = %s' % n
                self.cursor.execute(Sql_request)
                Kn = float(self.cursor.fetchone()[0])
            else:
                i = 0
                while index == 0:
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
                Kn = (first + second) / 2
        Kn = float('%.3f' % Kn)
        print('Kn = '+ str(Kn))

    # ОПРЕДЕЛЕНИЕ Cya max профиля ПО ГРАФИКУ

    # ОПРЕДЕНИЕ КОЭФ Cyamax
    def ChooseCymaxprof(self, c_, Re):
        # Выборка
        print('Re = '+str(Re))
        print('c_ = '+str(c_))
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
                Cyamaxprof = float(self.cursor.fetchone()[0])
                return Cyamaxprof
            elif Re > 8:
                Sql_request = 'SELECT Cyamaxprof FROM Коэф_Cyamaxprof ' \
                              'WHERE Re = %s AND Толщина= %s' % (8, c_)
                self.cursor.execute(Sql_request)
                Cyamaxprof = float(self.cursor.fetchone()[0])
                return Cyamaxprof
            else:
                i = 0
                index = 0
                while index == 0:
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
                Cyamaxprof = float('%.3f' % ((first + second) / 2))
                return Cyamaxprof

    def find_Cyamaxprof(self):
        global Cyamaxprof
        v0 = 0.000014607  # коэф кинематической вязкости на высоте 0
        # определение числа Рейнольдса
        Vmin = 3.5 * math.sqrt(Gpol / S)
        Re_full = (Vmin * b) / v0
        Re = float('%.1f' % (Re_full / 10 ** 6))

        # Вызов функции
        list_c_ = [0.08, 0.1, 0.12, 0.14, 0.16, 0.18, 0.2]
        if c_ in list_c_:
            Cyamaxprof = self.ChooseCymaxprof(c_, Re)
            print('Cyamaxprof = '+ str(Cyamaxprof))
        else:
            i = 0
            index = 0
            while index == 0:
                if list_c_[i] < c_ < list_c_[i + 1]:
                    index = i
                else:
                    i = i + 1
            first = self.ChooseCymaxprof(list_c_[index], Re)
            second = self.ChooseCymaxprof(list_c_[index + 1], Re)
            Cyamaxprof = float('%.3f' % ((first + second) / 2))
            print('Cyamaxprof = '+ str(Cyamaxprof))

    # ОПРЕДЕЛЕНИЕ приращения взлетного угла
    def find_da0_vzl(self, bzak_):
        global deltavzl
        print('deltavzl = ' + str(deltavzl))
        list_b_ = [0.1,0.2,0.3]
        list_delta = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3]
        if bzak_ in list_b_:
            if bzak_ == 0.1 and 0 <= deltavzl <= 0.6:
                return 0.158 * deltavzl + 0.0022
            elif bzak_ == 0.2 and 0 <= deltavzl <= 0.5:
                return 0.225 * deltavzl + 0.0125
            elif deltavzl in list_delta:
                Sql_request = 'SELECT delta_a0 FROM "Приращение взлетного угла" ' \
                              'WHERE b_zak = %s AND бvzl_pos= %s' % (bzak_, deltavzl)
                self.cursor.execute(Sql_request)
                return float(self.cursor.fetchone()[0])
            elif deltavzl > 1.3:
                Sql_request = 'SELECT delta_a0 FROM "Приращение взлетного угла" ' \
                              'WHERE b_zak = %s AND бvzl_pos= %s' % (bzak_, 1.3)
                self.cursor.execute(Sql_request)
                return float(self.cursor.fetchone()[0])
            else:
                i = 0
                index = 0
                while index == 0:
                    if list_delta[i] < deltavzl < list_delta[i + 1]:
                        index = i
                    else:
                        i = i + 1
                Sql_request = 'SELECT delta_a0 FROM "Приращение взлетного угла" ' \
                              'WHERE b_zak = %s AND бvzl_pos= %s' % (bzak_, list_delta[index])
                self.cursor.execute(Sql_request)
                first = float(self.cursor.fetchone()[0])
                # print(first)
                Sql_request = 'SELECT delta_a0 FROM "Приращение взлетного угла" ' \
                              'WHERE b_zak = %s AND бvzl_pos= %s' % (bzak_, list_delta[index+1])
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

    def pressedDown(self):
        self.main.tabWidget.setCurrentIndex(3)

    def pressedCre(self):
        self.main.tabWidget.setCurrentIndex(4)

    # РАСЧЕТ ИСХОДНЫХ ДАННЫХ КРЫЛА
    def CalculateWing(self):

        # Хорда средняя
        global l, S, b
        l = float(self.main.ed_l.text())
        S = float(self.main.ed_S.text())
        b = float('%.3f' % (S / l))
        self.main.ed_b.setText(str(b))

        # Сужение
        global b0, bk, n
        b0 = float(self.main.ed_b0.text())
        bk = float(self.main.ed_bk.text())
        n = float('%.2f' % (b0 / bk))
        self.main.ed_n.setText(str(n))

        # Относительная толщина профиля
        global cmax, c_
        cmax = float(self.main.ed_cmax.text())
        c_ = float('%.3f' % (cmax / b))
        self.main.ed_c_.setText(str(c_))

        # Относительная координата максимальной толщины
        global xc, xc_
        xc = float(self.main.ed_xc.text())
        xc_ = float('%.3f' % (xc / b))
        self.main.ed_xc_.setText(str(xc_))

        # Относительная кривизна профиля
        global fmax, f_
        fmax = float(self.main.ed_fmax.text())
        f_ = float('%.3f' % (100 * fmax / b))
        self.main.ed_f_.setText(str(f_))

        # Угол атаки нулевой подъемной силы
        global a0
        expression = (-1) * 0.9 * f_
        a0 = float('%.3f' % expression)
        self.main.ed_a0.setText(str(a0))

        # Относительная координата фокуса профиля
        global xf, xf_
        xf = float(self.main.ed_xf.text())
        xf_ = float('%.3f' % (xf / b))
        self.main.ed_xf_.setText(str(xf_))

        # Удлинение геометрическое
        global lamda
        lamda = float('%.3f' % (l ** 2 / S))
        self.main.ed_lamda.setText(str(lamda))

        # Относительная площадь, занятая фюзеляжем
        global Sf, Sf_
        Sf = float(self.main.ed_Sf.text())
        Sf_ = float('%.3f' % (Sf / S))
        self.main.ed_Sf_.setText(str(Sf_))

        # Относительная площадь, занятая гондолами двигателей
        global Sgd, Sgd_
        Sgd = float(self.main.ed_Sgd.text())
        Sgd_ = float('%.3f' % (Sgd / S))
        self.main.ed_Sgd_.setText(str(Sgd_))

        # Относительная площадь, занятая гондолами шасси
        global Sgsh, Sgsh_
        Sgsh = float(self.main.ed_Sgsh.text())
        Sgsh_ = float('%.3f' % (Sgsh / S))
        self.main.ed_Sgsh_.setText(str(Sgsh_))

        # Относительная площадь, не обтекаемая потоком
        global S_
        S_ = round(Sf_ + Sgd_ + Sgsh_, 3)
        self.main.ed_S_.setText(str(S_))

        # Удлинение эффективное
        global lamdaef, Kx, x_degree
        x_degree = int(self.main.ed_x_deg.text())
        self.find_Kx(n, x_degree)
        expression = (lamda * Kx) / (1 + S_)
        lamdaef = float('%.3f' % expression)
        self.main.ed_lamdaef.setText(str(lamdaef))

        # Производная коэф подъемной силы по углу атаки
        global caya, xc_degree
        xc_degree = float(self.main.ed_Sgsh.text()) * math.pi / 180
        expression = (2 * math.pi * lamdaef * math.cos(xc_degree)) / (57.3 * (lamdaef + 2 * math.cos(xc_degree)))
        caya = float('%.3f' % expression)
        self.main.ed_caya.setText(str(caya))  # есть разница !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        # Относительная площадь, обдуваемая винтами
        global Sobd, Sobd_
        Sobd = float(self.main.ed_Sobd.text())
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
        h = float(self.main.ed_h.text())

    # РАСЧЕТ ЗАКРЫЛОК И ПРЕДКРЫЛОК
    def CalculateFlapMulard(self):

        # Определение переменных
        global xshzak
        xshzak = float(self.main.ed_xshzak.text())

        # Относительная хорда закрылки
        global bzak, bzak_
        bzak = float(self.main.ed_bzak.text())
        bzak_ = float('%.2f' % (bzak / b))
        self.main.ed_bzak_.setText(str(bzak_))

        # Относ площадь крыла, обслуживаемая закрылками
        global Sobzak, Sobzak_
        Sobzak = float(self.main.ed_Sobzak.text())
        Sobzak_ = float('%.3f' % (Sobzak / S))
        self.main.ed_Sobzak_.setText(str(Sobzak_))

        # Хорда средняя крыла с выпущенными закрылком
        global bsrzak, lzak
        lzak = float(self.main.ed_lzak.text())
        bsrzak = float('%.3f' % (Sobzak / lzak))
        self.main.ed_bsrzak.setText(str(bsrzak))

        # Расстояние от края закрылка до земли при взлете
        global deltavzl, hvzl
        deltavzl = float(self.main.ed_deltavzl.text()) * math.pi / 180
        hvzl = ('%.3f' % (h - math.sin(deltavzl) * bzak))  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.main.ed_hvzl.setText(str(hvzl))

        # Расстояние от края закрылка до земли при посадке
        global deltapos, hpos
        deltapos = float(self.main.ed_deltapos.text()) * math.pi / 180
        hpos = ('%.3f' % (h - math.sin(deltapos) * bzak))  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.main.ed_hpos.setText(str(hpos))

        # Относ площадь крыла, обслуживаемая предкрылком
        global Sobpr, Sobpr_
        Sobpr = float(self.main.ed_Sobpr.text())
        Sobpr_ = float('%.3f' % (Sobpr / S))
        self.main.ed_Sobpr_.setText(str(Sobpr_))

    # РАСЧЕТ ГОРИЗОНТ И ВЕРТИКАЛ ОПЕРЕНИЯ
    def CalculateTail(self):
        # Определение переменных
        global bgo, xgo, bv, Sv, bvo, lvo, Svo
        bgo = float(self.main.ed_bgo.text())
        xgo = float(self.main.ed_xgo.text())
        bv = float(self.main.ed_bv.text())
        Sv = float(self.main.ed_Sv.text())
        bvo = float(self.main.ed_bvo.text())
        lvo = float(self.main.ed_lvo.text())
        Svo = float(self.main.ed_Svo.text())

        # Относительная толщина горизонт и вертикал оперения
        global cgo_, cvo_
        cvo_ = cgo_ = c_ - 0.02
        self.main.ed_cgo_.setText(str(cgo_))
        self.main.ed_cvo_.setText(str(cvo_))

        # Удлинение гор оперения
        global lgo, Sgo, lamdago
        lgo = float(self.main.ed_lgo.text())
        Sgo = float(self.main.ed_Sgo.text())
        lamdago = float('%.3f' % (lgo ** 2 / Sgo))
        self.main.ed_lamdago.setText(str(lamdago))

    # ОПРЕДЕЛЕНИЕ ПЕРЕМЕННЫХ ПИЛОНА
    def CalculatePylon(self):
        global bp, cp_, Sp
        bp = float(self.main.ed_bp.text())
        cp_ = float(self.main.ed_cp_.text())
        Sp = float(self.main.ed_Sp.text())

    # РАСЧЕТ ДАННЫХ ФЮЗЕЛЯЖА
    def CalculateFuselage(self):
        # Диаметр миделя
        global Df, Smf
        Smf = float(self.main.ed_Smf.text())
        Df = float('%.3f' % (math.sqrt(4 * Smf / math.pi)))
        self.main.ed_Df.setText(str(Df))

        # Удлинение
        global lamdaf, lf
        lf = float(self.main.ed_lf.text())
        lamdaf = float('%.3f' % (lf / Df))
        self.main.ed_lamdaf.setText(str(lamdaf))

        # Смоченная поверхность
        global Ssm
        Ssm = float('%.3f' % (2.5 * lf * Df))
        self.main.ed_Ssm.setText(str(Ssm))

        # Удлинение носовой части
        global lnf, lamdanf
        lnf = float(self.main.ed_lnf.text())
        lamdanf = float('%.3f' % (lnf / Df))
        self.main.ed_lamdanf.setText(str(lamdanf))

    # РАСЧЕТ ДАННЫХ ГОНДОЛ ДВИГАТЕЛЯ И ШАССИ
    def CalculateGondola(self):

        # Удлинение гондола двигателя
        global lgd, Dgd, lamdagd
        lgd = float(self.main.ed_lgd.text())
        Dgd = float(self.main.ed_Dgd.text())
        lamdagd = float('%.3f' % (lgd / Dgd))
        self.main.ed_lamdagd.setText(str(lamdagd))

        # Удлинение смоченная поверхность гондола двигателя
        global Ssm_gd
        Ssm_gd = float('%.3f' % (2.5 * lgd * Dgd))
        self.main.ed_Ssmgd.setText(str(Ssm_gd))

        # Удлинение удлинение носовой части гондола двигателя
        global ln_gd, lamdan_gd
        ln_gd = float(self.main.ed_lngd.text())
        lamdan_gd = float('%.3f' % (ln_gd / Dgd))
        self.main.ed_lamdangd.setText(str(lamdan_gd))

        # Удлинение гондола шасси
        global lgsh, Dgsh, lamdagsh
        lgsh = float(self.main.ed_lgsh.text())
        Dgsh = float(self.main.ed_Dgsh.text())
        lamdagsh = float('%.3f' % (lgsh / Dgsh))
        self.main.ed_lamdagsh.setText(str(lamdagsh))

        # Удлинение смоченная поверхность гондола шасси
        global Ssm_gsh
        Ssm_gsh = float('%.3f' % (2.5 * lgsh * Dgsh))
        self.main.ed_Ssmgsh.setText(str(Ssm_gsh))

        # Удлинение удлинение носовой части гондола шасси
        global ln_gsh, lamdan_gsh
        ln_gsh = float(self.main.ed_lngsh.text())
        lamdan_gsh = float('%.3f' % (ln_gsh / Dgsh))
        self.main.ed_lamdangsh.setText(str(lamdan_gsh))

    # СОХРАНЕНИЕ ОБЩИХ ДАННЫХ
    def SafeCommonData(self):
        global Gvzl, V, number, P0, H
        Gvzl = float(self.main.ed_Gvzl.text())
        V = float(self.main.ed_V.text())
        number = float(self.main.ed_number.text())
        P0 = float(self.main.ed_P0.text())
        H = float(self.main.ed_H.text())
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

    #
    def MakeMkr(self):
        self.main.tabWidget.setCurrentIndex(0)
        # Расчет координат вспомогательной прямой
        arr_cya = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
        arr_Mkr = []
        for cya in arr_cya:
            expression = 1 - 0.445 * math.pow(lamdaef - 1, 1 / 9) * (0.175 + 3.25 * c_) * (
                        math.cos(x_degree * math.pi / 180) + (0.365 * cya ** 2) / math.cos(
                    x_degree * math.pi / 180) ** 5)
            arr_Mkr.append(float('%.3f' % expression))
        print('Mkr = ' + str(arr_Mkr))

        # Занесение координат в БД
        arr = []
        arr_ =[0,1]
        for i in range(8):
            arr_[0] = arr_cya[i]
            arr_[1] = arr_Mkr[i]
            arr.append(tuple(arr_))
        cor = tuple(arr)
        # print(cor)
        self.cursor.execute('DELETE FROM "Кривая зависимость Мкр";',)
        sqlite_insert_query = """INSERT INTO 'Кривая зависимость Мкр'
                                         (Cya, Мкр) VALUES (?, ?);"""
        self.cursor.executemany(sqlite_insert_query, cor)
        self.connection.commit()

        # Отображение в приложении
        self.cursor.execute('''SELECT * FROM "Кривая зависимость Мкр" ''')
        # print(self.cursor.fetchall())

        # for index, form in enumerate(self.cursor.fetchall()):
        #     i = 0
        #     for item in form:
        #         print(str(item))
        #         self.tableWidget_Mkr.setItem(index, i, QTableWidgetItem(str(item)))
        #         i = i + 1
        #     self.tableWidget_Mkr.insertRow(1)

        # Расчет точки ?????
        Vms = float('%.3f' % (V / 3.6)) # км/ч в м/с
        Mrasch = float('%.4f' % (Vms / aH)) # определение расчетного числа маха
        global Gpol
        Gpol = Gvzl - 0.5 * Gm
        cya_rasch = float('%.4f' % ((2 * Gpol * g) / (pH * Vms * Vms * S)))

        print('cya_rasch = '+ str(cya_rasch))
        print('Mrasch = ' + str(Mrasch))

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        # plot data
        ax.plot(arr_cya, arr_Mkr)
        ax.plot(cya_rasch, Mrasch, marker='.')
        self.canvas.draw()

    # ПОСТРОЕНИЕ ВСПОМОГАТЕЛЬНОЙ КРИВОЙ cya = f(a)
    def MakeHelp(self):
        self.main.tabWidget.setCurrentIndex(1)
        self.fhelp.clear()
        ax = self.fhelp.add_subplot(111)

        # Линейный участок, характеризующий безотрывное обтекания крыла
        alfa_px2 = 5 # произвольно
        cya_py2 = caya * (alfa_px2 - a0)

        # Коэф cya max
        global Cyamax
        self.find_Kn(n)
        # print(Kn)
        self.find_Cyamaxprof()
        Cyamax = float ('%.3f' % (Cyamaxprof * Kn * (1 + math.cos(x_degree * math.pi/180))/ 2))
        cya_py3 = 0.85 * Cyamax
        print('Cyamax = ' + str(Cyamax))

        px3 = (cya_py3*(alfa_px2 - a0) + a0*cya_py2)/cya_py2
        # print(px3)
        px4 = (Cyamax*(alfa_px2 - a0) + a0*cya_py2)/cya_py2
        # print(px4)
        py = Cyamax - (Cyamax-cya_py3)

        deltaalfa= 2 # !!! произвольно
        px5 = px4 + deltaalfa

        arrX = [a0, alfa_px2, px3, px4]
        arrY = [0, cya_py2, cya_py3, py]
        # plot data
        ax.plot(arrX, arrY)
        ax.plot(a0, 0, marker='.')
        ax.plot(alfa_px2, cya_py2, marker='.')
        ax.plot(px3, cya_py3, marker='.')
        ax.plot(px4, Cyamax, marker='.')
        ax.plot(px5, Cyamax, marker='.')
        arc = matplotlib.patches.Arc((px5, cya_py3), deltaalfa*2, (Cyamax-cya_py3)*2, 180, 270)


        ax.add_patch(arc)
        self.chelp.draw()

    def MakeUp(self):
        self.main.tabWidget.setCurrentIndex(2)
        dCyamax_pr = 0
        global g
        da0_vzl=0
        # Преращение коэф подъем силы от выпуска предкрылков
        if Sobpr_ != 0:
            dCyamax_pr = 0.6*Sobpr_
            print('dCyamax_pr = '+ str(dCyamax_pr))
        # Преращение коэф подъем силы от выпуска закрылков
        list_bzak_ = [0.1, 0.2, 0.3]
        if Sobzak_ != 0:
            if bzak_ in list_bzak_:
                da0_vzl =(-1)*  self.find_da0_vzl(bzak_)
                print('da0_vzl=' + str(da0_vzl))
            elif bzak_ > 0.3:
                da0_vzl =(-1)*  self.find_da0_vzl(0.3)
                print('da0_vzl=' + str(da0_vzl))
            else:
                i = 0
                index = 0
                while index == 0:
                    if list_bzak_[i] < bzak_ < list_bzak_[i + 1]:
                        index = i
                        first = self.find_da0_vzl(list_bzak_[index])
                        second = self.find_da0_vzl(list_bzak_[index + 1])
                        if (bzak_*100) % 10 == 5:
                            da0_vzl =(-1)* float('%.3f' % ((first + second) / 2))
                            print('da0_vzl=' + str(da0_vzl))
                        elif (bzak_ * 100) % 10 < 5:
                            middle_a0_vzl= float('%.3f' % ((first + second) / 2))
                            da0_vzl = (-1)* float('%.3f' % ((first + middle_a0_vzl) / 2))
                            print('da0_vzl=' + str(da0_vzl))
                        elif (bzak_ * 100) % 10 > 5:
                            middle_a0_vzl = float('%.3f' % ((first + second) / 2))
                            da0_vzl = (-1)* float('%.3f' % ((second + middle_a0_vzl) / 2))
                            print('da0_vzl=' + str(da0_vzl))
                    else:
                        i = i + 1
            dCyamax=1.4
            if da0_vzl !=0:
                dCyamax_zak_vzl=4.83*dCyamax*Sobzak_* abs((-1)*da0_vzl)*math.cos(xshzak*math.pi/180)*math.cos(xshzak*math.pi/180)
           # УРАВНЕНИЯ ПРИ НАЛИЧИИ ВИНТОВ
           # if Sobd_ != 0
                Cyamax_vzl = Cyamax +  dCyamax_pr +  dCyamax_zak_vzl # +dCya_obd
                a0_vzl = (a0+ da0_vzl*180/math.pi)#+da0_obd
                print('dCyamax_zak_vzl= '+ str(dCyamax_zak_vzl))
                print('Cyamax_vzl= '+ str(Cyamax_vzl))
                print('a0_vzl= '+ str(a0_vzl))








if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    # window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение
