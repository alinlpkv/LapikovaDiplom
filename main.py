import sqlite3
import PyQt5
import sys  # sys нужен для передачи argv в QApplication
import matplotlib.patches
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QVBoxLayout, QTableWidgetItem, QHBoxLayout, QGridLayout, QLabel, QMessageBox
# from matplotlib.backends.backend_template import FigureCanvas
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from UI import Ui_MainWindow  # Это наш конвертированный файл дизайна
# pyuic5 UI.ui -o UI.py
import math
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate
from UI_Choose import Ui_Form
from UI_dialog import Ui_Dialog
from prettytable import PrettyTable

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
dCxomax = 0

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
ngo = 0
nvo = 0

# Pylon
bp = 0
cp_ = 0
Sp = 0
npylon = 0

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
ngd = 0
ngsh = 0

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
Kint = 0
cxk_light = 0
nlight = 0

# ВЕЛИЧИНЫ ИЗ ГРАФИКОВ
Kx = 0
Kn = 0
Cyamaxprof = 0

# ВЕЛИЧИНЫ ИЗ ТАБЛИЦ
pH = 0  # массовая плотность
aH = 0  # скорость звука
vH = 0 # вязкость воздуха
Gm = 0  # полный запас топлива

dCyamax = 0  # по типу закрылка

# CONST
g = 9.8
p_zero = 1.225  # плотность воздуха на нулевой высоте
v_zero = 1.4607 * math.pow(10, -5)  # коэф кинематической вязкости на нулевой высоте

# ВЫСЧИТАННЫЕ
Mrasch = 0  # число Маха расчетное
Gpol = 0  # полетный вес самолета
Cyamax = 0
da0_vzl = 0
# Вспомогательная кривая
Re = 0
Vmin = 0

# взлетная кривая


# для интерфейса
permision_for_curve = [False, False, False]

# для таблиц
# вспомогательная поляра
linear_size = []
S_proiz=[]
c_lamda_el_for_cxa = []
Sk_el_for_cxa = []
n_el_for_cxa = []
a_list_help=[]
cya_list_help=[]
cxo=0
xtau_el_for_cxa = []

# взлетная поляра
a_list_up=[]
cya_list_up=[]
Cyamax_vzl =0
a_list_up_scrin=[]
cya_list_up_scrin=[]
Cyamax_vzl_scrin=0
lamdaef_scrin=0

# посадочная кривая
a_list_down=[]
cya_list_down=[]
Cya_max_pos =0
a_list_down_scrin=[]
cya_list_down_scrin=[]
Cya_max_pos_scrin=0
lamdaef_down_scrin=0

# крейсерская
list_Mkr=[]

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
        else:
            msg_ = QMessageBox()
            msg_.setIcon(QMessageBox.Critical)
            msg_.setText("Выберите тип механизации.")
            msg_.setWindowTitle("Предупреждение")
            msg_.exec_()
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

        self.button = [self.main.buWing, self.main.buFlapMulard, self.main.buTail, self.main.buPylon,
                       self.main.buGondola, self.main.buFuselage, self.main.buCommonData]
        self.button_curve = [self.main.buMkr, self.main.buHelp, self.main.buUp, self.main.buDown, self.main.buCre]

        self.main.groupBox_13.setVisible(False)
        self.main.buHelp.setVisible(False)
        self.main.buUp.setVisible(False)
        self.main.buDown.setVisible(False)
        self.main.buCre.setVisible(False)
        self.main.tabData.setTabEnabled(1, False)
        self.main.tabData.setTabEnabled(2, False)

        # График для Мкр
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(NavigationToolbar(self.canvas, self))
        layout.addWidget(self.canvas)
        # layout.addWidget(str.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft))

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

        # График для вспомогательной поляры
        self.fP_Help = plt.figure()
        self.cP_Help = FigureCanvas(self.fP_Help)
        Vlayout_P_Help = QVBoxLayout()
        Vlayout_P_Help.addWidget(NavigationToolbar(self.cP_Help, self))
        Vlayout_P_Help.addWidget(self.cP_Help)
        self.main.helpwidget_2.setLayout(Vlayout_P_Help)

        # График для взлетной поляры
        self.fP_Up = plt.figure()
        self.cP_Up = FigureCanvas(self.fP_Up)
        Vlayout_P_Up = QVBoxLayout()
        Vlayout_P_Up.addWidget(NavigationToolbar(self.cP_Up, self))
        Vlayout_P_Up.addWidget(self.cP_Up)
        self.main.upwidget_2.setLayout(Vlayout_P_Up)

        # График для посадочной поляры
        self.fP_Down = plt.figure()
        self.cP_Down = FigureCanvas(self.fP_Down)
        Vlayout_P_Down = QVBoxLayout()
        Vlayout_P_Down.addWidget(NavigationToolbar(self.cP_Down, self))
        Vlayout_P_Down.addWidget(self.cP_Down)
        self.main.downwidget_2.setLayout(Vlayout_P_Down)

        # График для крейсерских и полетных поляр
        self.fP_Cre = plt.figure()
        self.cP_Cre = FigureCanvas(self.fP_Cre)
        Vlayout_P_Cre = QVBoxLayout()
        Vlayout_P_Cre.addWidget(NavigationToolbar(self.cP_Cre, self))
        Vlayout_P_Cre.addWidget(self.cP_Cre)
        self.main.cruiswidget_2.setLayout(Vlayout_P_Cre)

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
        self.main.buCre.clicked.connect(self.pressedPolyr)


        # вторая вкладка
        self.main.tabWidget.setTabVisible(0, False)
        self.main.tabWidget.setTabVisible(1, False)
        self.main.tabWidget.setTabVisible(2, False)
        self.main.tabWidget.setTabVisible(3, False)
        self.main.tabWidget.setTabVisible(4, False)

        # третья вкладка
        self.main.tabPolyr.setTabVisible(0,False)
        self.main.tabPolyr.setTabVisible(1,False)
        self.main.tabPolyr.setTabVisible(2,False)
        self.main.tabPolyr.setTabVisible(3,False)

        # Построение вспомогательных кривых
        self.main.buMkr.clicked.connect(self.MakeMkr)
        self.main.buHelp.clicked.connect(self.MakeHelp)
        self.main.buUp.clicked.connect(self.MakeUp)
        self.main.buDown.clicked.connect(self.MakeDown)
        self.main.buCre.clicked.connect(self.MakeCruise)

        # Построение поляр
        self.main.buHelpPolyr.clicked.connect(self.MakeHelpPolyr)
        self.main.buUpPolyr.clicked.connect(self.MakeUpPolyr)
        self.main.buDownPolyr.clicked.connect(self.MakeDownPolyr)
        self.main.buCrePolyr.clicked.connect(self.MakeCruisePolyr)

        # Расчет переменных
        self.main.buCalWing.clicked.connect(self.CalculateWing)
        self.main.buCalFlapMulard.clicked.connect(self.CalculateFlapMulard)
        self.main.buCalTail.clicked.connect(self.CalculateTail)
        self.main.buCalPylon.clicked.connect(self.CalculatePylon)
        self.main.buCalFuselage.clicked.connect(self.CalculateFuselage)
        self.main.buCalGondola.clicked.connect(self.CalculateGondola)
        self.main.buCommonDataSafe.clicked.connect(self.SafeCommonData)

    def ButtonEnabled(self):
        self.main.groupBox_13.setVisible(True)
        self.pressedWing()


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

    # ОПРЕДЕЛЕНИЕ рН, аН, vH ПО ТАБЛИЦЕ
    def find_with_H(self, H):
        global pH, aH, vH
        pH = 0
        aH = 0
        vH = 0
        h = float('%.1f' % (H / 1000))

        Sql_request = 'SELECT * FROM "Стандартная_атмосфера" ' \
                      'WHERE "Высота(км)" = %s' % str(h)
        self.cursor.execute(Sql_request)
        cor = self.cursor.fetchone()
        # print(cor)
        pHstr = cor[3]
        aHstr = cor[6]
        vHstr = cor[5]

        pH = float(pHstr)
        aH = float(aHstr)
        vH = float(vHstr)

        print('pH = ' + str(pH))
        print('aH = ' + str(aH))
        print('vH = ' + str(vH))

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

    # ОПРЕДЕЛЕНИЕ КОЭФФИЦИЕНТА СОПРОТИВЛЕНИЯ ТРЕНИЯ ПЛОСКОЙ ПЛАСТИНЫ 2Cf
    def find_2cf(self, xt, Re):
        list_Re = [1, 2, 5, 10, 20, 50, 100, 200, 500]
        list_xt = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 1]
        two_cf = 0
        const_v = 0

        if xt == 0.1:
            xt = 0
            if Re >= 11:
                const_v = 0.00025
            else:
                const_v = 0.0004
        # для необозначенных на графике точек перехода
        elif 0.5 < xt < 1:
            multip = (xt - 0.5) * 10
            xt = 0.5
            f = False
            i = 0
            while not f:
                if list_Re[i] <= Re < list_Re[i + 1]:
                    f = True
                    const_v = multip * (0.0007 - (0.000039 * i))
                elif Re == 500:
                    f = True
                    const_v = multip * (0.0007 - (0.000039 * 9))
                elif Re < 1:
                    f = True
                    const_v = multip * (0.0007 - (0.000039 * 0))
                else:
                    i = i + 1

        if xt in list_xt:
            try:
                two_cf = self.request_Kcf(xt, Re)
            except TypeError:
                flag = False
                i = 0
                while not flag:
                    if list_Re[i] < Re < list_Re[i + 1]:
                        flag = True
                        y1 = self.request_Kcf(xt, list_Re[i])
                        y2 = self.request_Kcf(xt, list_Re[i + 1])
                        two_cf = self.cal_system(list_Re[i], y1, list_Re[i + 1], y2, Re)
                    elif Re > 500:
                        two_cf = self.request_Kcf(xt, 500)
                        flag = True
                    elif Re < 1:
                        two_cf = self.request_Kcf(xt, 1)
                        flag = True
                    else:
                        i = i + 1
        else:
            if xt > 1:
                return self.find_2cf(1, Re)
            # для не целых точек перехода
            else:
                flag = False
                i = 0
                while not flag:
                    if list_xt[i] < xt < list_xt[i + 1]:
                        flag = True
                        if xt - list_xt[i] >= 0.03 and list_xt[i + 1] - xt >= 0.03:
                            v1 = self.find_2cf(list_xt[i], Re)
                            v2 = self.find_2cf(list_xt[i + 1], Re)
                            two_cf = (v1 + v2) / 2
                        elif xt - list_xt[i] < 0.03:
                            two_cf = self.find_2cf(list_xt[i], Re)
                        else:
                            two_cf = self.find_2cf(list_xt[i + 1], Re)
                    else:
                        i = i + 1

        # print(two_cf)
        two_cf = float('%.5f' % (two_cf - const_v))
        return two_cf

    # Поиск коэффициентов системы функции и расчет значения
    def cal_system(self, x1, y1, x2, y2, x):
        k = (y1 - y2) / (x1 - x2)
        b_koef = y1 - k * x1
        return float('%.5f' % (k * x + b_koef))

    # SQL запрос для коэффицента 2Cf
    def request_Kcf(self, xt, Re):
        Sql_request = 'SELECT "2cf" FROM Коэф_cf ' \
                      'WHERE "Точка перехода" = %s AND "Re * 10^6"= %s' % (xt, Re)
        self.cursor.execute(Sql_request)
        return float(self.cursor.fetchone()[0])

    # ОПРЕДЕЛЕНИЕ КОЭФФИЦИЕНТА РЕЖИМА ТЕЧЕЧЕНИЯ В ПОГРАНИЧНОМ СЛОЕ ДЛЯ КРЫЛА
    def find_nc_wing(self, xt, c_):
        # list_c_ = [0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15]
        list_c_ = [float(i) for i in np.arange(0, 0.16, 0.01)]
        cur = self.request_nc_wing(c_)
        if cur is None:
            if c_ > 0.15:
                cur = self.request_nc_wing(0.15)
            elif c_ < 0.01:
                cur = self.request_nc_wing(0)
            else:
                flag = False
                i = 0
                while not flag:
                    if list_c_[i] < c_ < list_c_[i + 1]:
                        y1_cur = self.request_nc_wing(list_c_[i])
                        y2_cur = self.request_nc_wing(list_c_[i + 1])
                        y1 = y1_cur[1] - xt * 10 * y1_cur[2]
                        y2 = y2_cur[1] - xt * 10 * y2_cur[2]
                        return self.cal_system(list_c_[i], y1, list_c_[i + 1], y2, c_)
                    else:
                        i = i + 1

        nc = float('%.4f' % (cur[1] - xt * 10 * cur[2]))
        if nc < 1:
            nc = 1

        return nc

    # SQL запрос для коэффицента nc для крыла
    def request_nc_wing(self, c_):
        Sql_request = 'SELECT * FROM Коэф_nc_крыло WHERE "c_"= %s' % c_
        self.cursor.execute(Sql_request)
        return self.cursor.fetchone()

    # ОПРЕДЕЛЕНИЕ КОЭФФИЦИЕНТА РЕЖИМА ТЕЧЕЧЕНИЯ В ПОГРАНИЧНОМ СЛОЕ ДЛЯ ТЕЛ ВРАЩЕНИЯ
    def find_nc_body_rotate(self, lamda):
        list_lamda = [2.25, 2.6, 3.2, 4, 4.8, 6, 8, 10, 12, 14]
        if lamda in list_lamda:
            return self.request_nc_body_rotate(lamda)
        elif lamda > 14:
            return self.request_nc_body_rotate(14)
        elif lamda < 2.25:
            return self.request_nc_body_rotate(2.25)
        else:
            flag = False
            i = 0
            while not flag:
                if list_lamda[i] < lamda < list_lamda[i + 1]:
                    y1 = self.request_nc_body_rotate(list_lamda[i])
                    y2 = self.request_nc_body_rotate(list_lamda[i + 1])
                    return self.cal_system(list_lamda[i], y1, list_lamda[i + 1], y2, lamda)
                else:
                    i = i + 1

    # SQL запрос для коэффицента nc для крыла
    def request_nc_body_rotate(self, lamda):
        Sql_request = 'SELECT nc FROM Коэф_nc_тело_вращения WHERE "lamda"= %s' % lamda
        self.cursor.execute(Sql_request)
        return self.cursor.fetchone()[0]

    def iconbutton(self, bufill, buttons):
        for bu in buttons:
            bu.setIcon(QtGui.QIcon('caret-right.svg'))
        if S == 0 and b == 0:
            self.main.buFlapMulard.setIcon(QtGui.QIcon('x.svg'))
        bufill.setIcon(QtGui.QIcon('caret-right-fill.svg'))

    # ОПРЕДЕЛЕНЕ КОЭФФИЦИЕНТА Кинт
    def request_Kint(self, type):
        Sql_request = 'SELECT "Кинт" FROM "Коэф_Кинт" WHERE "Форма" = %s' % str('"' + type + '"')
        self.cursor.execute(Sql_request)
        return self.cursor.fetchone()[0]

    # ОПРЕДЕЛЕНЕ КОЭФФИЦИЕНТА cxk для фонаря
    def request_cxk(self, type):
        Sql_request = 'SELECT "cxk" FROM "Коэф_cxk" WHERE "Фонарь" = %s' % str('"' + type + '"')
        self.cursor.execute(Sql_request)
        return self.cursor.fetchone()[0]

    # ОПРЕДЕЛЕНИЕ ПОПРАВКИ
    def call_delta(self, lamda, n):
        list_lamda = [5, 7, 10]
        delta = 0

        if lamda in list_lamda:
            delta = self.find_delta(lamda, n)
        elif lamda > 10:
            delta = self.find_delta(10, n)
        elif lamda < 5:
            delta = self.find_delta(5, n)
        elif 5 < lamda < 7:
            first = self.find_delta(5, n)
            second = self.find_delta(7, n)
            part = (second - first) / 20
            print(lamda % 5)
            delta = (lamda % 5) * part * 10 + first
        elif 7 < lamda < 10:
            first = self.find_delta(7, n)
            second = self.find_delta(10, n)
            part = (second - first) / 30
            delta = (lamda % 7) * part * 10 + first

        return float('%.4f' % delta)

    def find_delta(self, lamda, n):
        list_n = [float(i) for i in np.arange(1.25, 5.25, 0.25)]
        delta = 0
        try:
            delta = self.request_delta(lamda, n)
        except:
            if n < 1.25:
                delta = self.request_delta(lamda, 1.25)
            elif n > 5:
                y1 = self.call_delta(lamda, 4.5)
                y2 = self.call_delta(lamda, 5)
                print(y1)
                print(y2)
                return self.cal_system(4.5, y1, 5, y2, n)
            else:
                flag = False
                i = 0
                while not flag:
                    if list_n[i] < n < list_n[i + 1]:
                        y1 = self.request_delta(lamda, list_n[i])
                        y2 = self.request_delta(lamda, list_n[i + 1])
                        return self.cal_system(list_n[i], y1, list_n[i + 1], y2, n)
                    else:
                        i += 1
        return float(delta)

    def request_delta(self, lamda, n):
        Sql_request = 'SELECT Дельта FROM Поправка ' \
                      'WHERE "Удлинение"= %s AND "Сужение"= %s' % (lamda, n)
        self.cursor.execute(Sql_request)
        return self.cursor.fetchone()[0]

    # ОПРЕДЕЛЕНИЕ КОЭФФИЦИЕНТА ПРИРАЩЕНИЯ ОТ ВЫПУЩЕННЫХ ЗАКРЫЛКОВ
    def find_dCxo_zak(self, bzak, delta):
        list_delta = [float('%.1f' % i) for i in np.arange(0, 0.9, 0.1)] # МОЖЕТ БЫТЬ 1 ???

        if (bzak == 0.3 or bzak == 0.1) and delta in list_delta:
            return self.request_dcxo(bzak, delta)
        elif bzak == 0.3 or bzak == 0.1:
            flag = False
            i = 0
            while not flag:
                if list_delta[i] < delta < list_delta[i + 1]:
                    y1 = self.request_dcxo(bzak, list_delta[i])
                    y2 = self.request_dcxo(bzak, list_delta[i + 1])
                    return self.cal_system(list_delta[i], y1, list_delta[i + 1], y2, delta)
                else:
                    i += 1
        else:
            first = self.find_dCxo_zak(0.1, delta)
            second = self.find_dCxo_zak(0.3, delta)
            part = (second - first) / 20
            dcxo_zak = (bzak - 0.1) * part * 100 + first
            return float('%.4f' % dcxo_zak)

    def request_dcxo(self, b, d):
        Sql_request = 'SELECT dcxo_zak FROM dCxo_zak ' \
                      'WHERE b_zak= %s AND delta= %s' % (b, d)
        self.cursor.execute(Sql_request)
        return self.cursor.fetchone()[0]


    # ОПРЕДЕЛЕНИЕ КОЭФ nM ТЕЛО ВРАЩЕНИЯ
    def call_nM_body_rotation(self, la_nch, M):
        list_la_nch = [1,2,3,4,5]
        nM = 0

        if la_nch in list_la_nch:
            nM = self.find_nM_body_rotation(la_nch, M)
        elif la_nch > 5:
            nM = self.find_nM_body_rotation(6, M)
        elif la_nch < 1:
            nM = self.find_nM_body_rotation(1, M)
        else:
            flag = False
            i = 0
            while not flag:
                if list_la_nch[i] < la_nch < list_la_nch[i + 1]:
                    first = self.find_nM_body_rotation(list_la_nch[i], M)
                    second = self.find_nM_body_rotation(list_la_nch[i+1], M)
                    #print(first)
                    #print(second)
                    part =  (first - second) / 10
                    nM = first - (la_nch - first) * part
                    flag = True
                else:
                    i += 1

        return float('%.4f' % nM)

    def find_nM_body_rotation(self, la_nch, M):
        list_M = [float('%.1f' % i) for i in np.arange(0.2, 1, 0.1)]
        nM = 0
        try:
            nM = self.request_nM_body_rotation(la_nch, M)
        except:
            if M < 0.2:
                nM = 1
            elif M > 0.9:
                y1 = self.call_nM_body_rotation(la_nch, 0.8)
                y2 = self.call_nM_body_rotation(la_nch, 0.9)
                return self.cal_system(0.8, y1, 0.9, y2, M)
            else:
                flag = False
                i = 0
                while not flag:
                    if list_M[i] < M < list_M[i + 1]:
                        y1 = self.request_nM_body_rotation(la_nch, list_M[i])
                        y2 = self.request_nM_body_rotation(la_nch, list_M[i + 1])
                        return self.cal_system(list_M[i], y1, list_M[i + 1], y2, M)
                    else:
                        i += 1
        return float(nM)

    def request_nM_body_rotation(self, la_nch, M):
        Sql_request = 'SELECT nM FROM Коэф_nM_тело_вращения ' \
                      'WHERE lamda_nch= %s AND M= %s' % (la_nch, M)
        self.cursor.execute(Sql_request)
        return self.cursor.fetchone()[0]

        # ОПРЕДЕЛЕНИЕ КОЭФ nM КРЫЛО
    def call_nM_wing(self, c_, M):
        list_c_ = [0,4,8,12,20]
        nM = 0

        if c_ in list_c_:
            nM = self.find_nM_wing(c_, M)
        elif c_ > 20:
            nM = self.find_nM_wing(20, M)
        else:
            flag = False
            i = 0
            while not flag:
                if list_c_[i] < c_ < list_c_[i + 1]:
                    first = self.find_nM_wing(list_c_[i], M)
                    second = self.find_nM_wing(list_c_[i + 1], M)
                    print(first)
                    print(second)
                    part = (second - first) / 40 #!!!!!!!
                    nM = (c_ % first) * part * 10 + first
                    flag = True
                else:
                    i += 1

        return float('%.4f' % nM)

    def find_nM_wing(self, c_, M):
        list_M = [float('%.1f' % i) for i in np.arange(0.2, 1, 0.1)]
        nM = 0
        try:
            nM = self.request_nM_wing(c_, M)
        except:
            if M < 0.2:
                nM = 1
            elif M > 0.9:
                y1 = self.call_nM_wing(c_, 0.8)
                y2 = self.call_nM_wing(c_, 0.9)
                return self.cal_system(0.8, y1, 0.9, y2, M)
            else:
                flag = False
                i = 0
                while not flag:
                    if list_M[i] < M < list_M[i + 1]:
                        y1 = self.request_nM_wing(c_, list_M[i])
                        y2 = self.request_nM_wing(c_, list_M[i + 1])
                        return self.cal_system(list_M[i], y1, list_M[i + 1], y2, M)
                    else:
                        i += 1
        return float(nM)

    def request_nM_wing(self, c_, M):
        Sql_request = 'SELECT nM FROM Коэф_nM_крыло ' \
                      'WHERE c_= %s AND M= %s' % (c_, M)
        self.cursor.execute(Sql_request)
        return self.cursor.fetchone()[0]

    # ОТКРЫТИЕ ВКЛАДОК ПО КНОПКАМ
    def pressedWing(self):
        self.main.tabWidget_2.setCurrentIndex(0)
        # v = self.find_2cf(0.4, 500)
        # print('2cf = '+str(v))
        # nc_wing = self.find_nc_wing(0.5, 0.16)
        # print('nc_wing = ' + str(nc_wing))
        # nc_br = self.find_nc_body_rotate(8)
        # print('nc_br = ' + str(nc_br))
        # print('delta = ' + str(self.call_delta(2.2, 13)))
        # print('dCxo_zak = ' + str(self.find_dCxo_zak(0.2, 0.68)))
        # print('nM тело = ' + str(self.call_nM_body_rotation(2.7, 0.95)))
        print('nM крыло = ' + str(self.call_nM_wing(6, 0.7)))

        self.iconbutton(self.main.buWing, self.button)

    def pressedFlapMulard(self):
        if b != 0 and S != 0:
            self.main.tabWidget_2.setCurrentIndex(1)
            self.iconbutton(self.main.buFlapMulard, self.button)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Сначала рассчитайте параметры крыла.")
            msg.setWindowTitle("Предупреждение")
            msg.exec_()

    def pressedTail(self):
        self.main.tabWidget_2.setCurrentIndex(2)
        self.iconbutton(self.main.buTail, self.button)

    def pressedPylon(self):
        self.main.tabWidget_2.setCurrentIndex(3)
        self.iconbutton(self.main.buPylon, self.button)

    def pressedFuselage(self):
        self.main.tabWidget_2.setCurrentIndex(4)
        self.iconbutton(self.main.buFuselage, self.button)

    def pressedGondola(self):
        self.main.tabWidget_2.setCurrentIndex(5)
        self.iconbutton(self.main.buGondola, self.button)

    def pressedCommonData(self):
        self.main.tabWidget_2.setCurrentIndex(6)
        self.iconbutton(self.main.buCommonData, self.button)

    def pressedPolyr(self):
        self.main.tabData.setTabEnabled(2, True)

    def OpenPlan(self):
        dlg = DialogPlan(self)
        dlg.show()

    def OpenFlapChoose(self):
        dialog = DialogMechanism(self)
        dialog.show()

    # РАСЧЕТ ИСХОДНЫХ ДАННЫХ КРЫЛА
    def CalculateWing(self):

        try:
            # Хорда средняя
            global l, S, b
            l = float(self.main.ed_l.text().replace(',', '.'))
            S = float(self.main.ed_S.text().replace(',', '.'))
            b = float('%.3f' % (S / l))
            self.main.ed_b.setText(str(b))
            if b != 0 and S != 0:
                self.main.buFlapMulard.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
                self.main.buFlapMulard.setStyleSheet("background-color: white;")

            # Сужение
            global b0, bk, n
            b0 = float(self.main.ed_b0.text().replace(',', '.'))
            bk = float(self.main.ed_bk.text().replace(',', '.'))
            n = float('%.2f' % (b0 / bk))
            self.main.ed_n.setText(str(n))

            # Относительная толщина профиля
            global cmax, c_
            cmax = float(self.main.ed_cmax.text().replace(',', '.'))
            c_ = float('%.2f' % (cmax / b))
            self.main.ed_c_.setText(str(c_))

            # Относительная координата максимальной толщины
            global xc, xc_
            xc = float(self.main.ed_xc.text().replace(',', '.'))
            xc_ = float('%.3f' % (xc / b))
            self.main.ed_xc_.setText(str(xc_))

            # Относительная кривизна профиля
            global fmax, f_
            fmax = float(self.main.ed_fmax.text().replace(',', '.'))
            f_ = float('%.3f' % (100 * fmax / b))
            self.main.ed_f_.setText(str(f_))

            # Угол атаки нулевой подъемной силы
            global a0
            expression = (-1) * 0.9 * f_
            a0 = float('%.3f' % expression)
            self.main.ed_a0.setText(str(a0))

            # Относительная координата фокуса профиля
            global xf, xf_
            xf = float(self.main.ed_xf.text().replace(',', '.'))
            xf_ = float('%.3f' % (xf / b))
            self.main.ed_xf_.setText(str(xf_))

            # Удлинение геометрическое
            global lamda
            lamda = float('%.3f' % (l ** 2 / S))
            self.main.ed_lamda.setText(str(lamda))

            # Относительная площадь, занятая фюзеляжем
            global Sf, Sf_
            Sf = float(self.main.ed_Sf.text().replace(',', '.'))
            Sf_ = float('%.3f' % (Sf / S))
            self.main.ed_Sf_.setText(str(Sf_))

            # Относительная площадь, занятая гондолами двигателей
            global Sgd, Sgd_
            Sgd = float(self.main.ed_Sgd.text().replace(',', '.'))
            Sgd_ = float('%.3f' % (Sgd / S))
            self.main.ed_Sgd_.setText(str(Sgd_))

            # Относительная площадь, занятая гондолами шасси
            global Sgsh, Sgsh_
            Sgsh = float(self.main.ed_Sgsh.text().replace(',', '.'))
            Sgsh_ = float('%.3f' % (Sgsh / S))
            self.main.ed_Sgsh_.setText(str(Sgsh_))

            # Относительная площадь, не обтекаемая потоком
            global S_
            S_ = round(Sf_ + Sgd_ + Sgsh_, 3)
            self.main.ed_S_.setText(str(S_))

            # Удлинение эффективное
            global lamdaef, Kx, x_degree
            x_degree = float(self.main.ed_x_deg.text().replace(',', '.'))
            self.find_Kx(n, x_degree)
            expression = (lamda * Kx) / (1 + S_)
            lamdaef = float('%.3f' % expression)
            self.main.ed_lamdaef.setText(str(lamdaef))

            # Производная коэф подъемной силы по углу атаки
            global caya, xc_degree
            xc_degree = float(self.main.ed_xc_deg.text().replace(',', '.'))
            if x_degree > 90 or xc_degree > 90:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Стреловидность не может быть больше 90 градусов.")
                msg.setWindowTitle("Ошибка")
                msg.exec_()
            else:
                xc_degree = float(self.main.ed_xc_deg.text().replace(',', '.')) * math.pi / 180
                expression = (2 * math.pi * lamdaef * math.cos(xc_degree)) / (
                        57.3 * (lamdaef + 2 * math.cos(xc_degree)))
                caya = float('%.3f' % expression)
                self.main.ed_caya.setText(str(caya))

                # Относительная площадь, обдуваемая винтами
                global Sobd, Sobd_
                Sobd = float(self.main.ed_Sobd.text().replace(',', '.'))
                Sobd_ = float('%.3f' % (Sobd / S))
                self.main.ed_Sobd_.setText(str(Sobd_))

                # Относительная координата точки перехода ЛПС в ТПС
                global xtau_
                if xc == 0:
                    expression = xc_ * (1 - Sobd_)
                else:
                    expression = 0
                xtau_ = float('%.3f' % expression)
                self.main.ed_xtau_.setText(
                    str(xtau_))  # У РЕБЯТ РАВНО 0 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

                # Коэффициент момента профиля
                global cmo
                cmo = float('%.3f' % ((-1) * 0.005 * math.pi * f_))
                self.main.ed_cmo.setText(str(cmo))

                # Определение переменных
                global h
                h = float(self.main.ed_h.text().replace(',', '.'))

            self.iconbutton(self.main.buWing, self.button)
            permision_for_curve[0] = True
        except ValueError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Неправильный ввод данных.")
            msg.setWindowTitle("Ошибка")
            msg.setDetailedText("Вводить можно только цифры. Числа должны быть положительными.")
            msg.exec_()

        if permision_for_curve[0] and permision_for_curve[1] and permision_for_curve[2]:
            self.main.tabData.setTabEnabled(1, True)

    # РАСЧЕТ ЗАКРЫЛОК И ПРЕДКРЫЛОК
    def CalculateFlapMulard(self):

        try:
            # Определение переменных
            global xshzak
            xshzak = float(self.main.ed_xshzak.text().replace(',', '.'))

            # Относительная хорда закрылки
            global bzak, bzak_
            bzak = float(self.main.ed_bzak.text().replace(',', '.'))
            bzak_ = float('%.2f' % (bzak / b))
            self.main.ed_bzak_.setText(str(bzak_))

            # Относ площадь крыла, обслуживаемая закрылками
            global Sobzak, Sobzak_
            Sobzak = float(self.main.ed_Sobzak.text().replace(',', '.'))
            Sobzak_ = float('%.3f' % (Sobzak / S))
            self.main.ed_Sobzak_.setText(str(Sobzak_))

            # Хорда средняя крыла с выпущенными закрылком
            global bsrzak, lzak
            lzak = float(self.main.ed_lzak.text().replace(',', '.'))
            bsrzak = float('%.3f' % (Sobzak / lzak))
            self.main.ed_bsrzak.setText(str(bsrzak))

            # Расстояние от края закрылка до земли при взлете
            global deltavzl, hvzl, deltapos
            deltavzl = float(self.main.ed_deltavzl.text().replace(',', '.'))
            deltapos = float(self.main.ed_deltapos.text().replace(',', '.'))
            if deltavzl >= 90 or deltapos >= 90:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Cлишком большой угол отклонения.")
                msg.setWindowTitle("Ошибка")
                msg.exec_()
            else:
                deltavzl = float(self.main.ed_deltavzl.text().replace(',', '.')) * math.pi / 180
                hvzl = float('%.3f' % (h - math.sin(deltavzl) * bzak))  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                self.main.ed_hvzl.setText(str(hvzl))

                # Расстояние от края закрылка до земли при посадке
                global hpos
                deltapos = float(self.main.ed_deltapos.text().replace(',', '.')) * math.pi / 180
                hpos = float('%.3f' % (h - math.sin(deltapos) * bzak))  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                self.main.ed_hpos.setText(str(hpos))

                # Относ площадь крыла, обслуживаемая предкрылком
                global Sobpr, Sobpr_
                Sobpr = float(self.main.ed_Sobpr.text().replace(',', '.'))
                Sobpr_ = float('%.3f' % (Sobpr / S))
                self.main.ed_Sobpr_.setText(str(Sobpr_))

            permision_for_curve[1] = True

        except ValueError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Неправильный ввод данных.")
            msg.setWindowTitle("Ошибка")
            msg.setDetailedText("Вводить можно только цифры. Числа должны быть положительными.")
            msg.exec_()

        if permision_for_curve[0] and permision_for_curve[1] and permision_for_curve[2]:
            self.main.tabData.setTabEnabled(1, True)

    # РАСЧЕТ ГОРИЗОНТ И ВЕРТИКАЛ ОПЕРЕНИЯ
    def CalculateTail(self):

        try:
            # Определение переменных
            global bgo, xgo, bv, Sv, bvo, lvo, Svo
            bgo = float(self.main.ed_bgo.text().replace(',', '.'))
            xgo = float(self.main.ed_xgo.text().replace(',', '.'))
            bv = float(self.main.ed_bv.text().replace(',', '.'))
            Sv = float(self.main.ed_Sv.text().replace(',', '.'))
            bvo = float(self.main.ed_bvo.text().replace(',', '.'))
            lvo = float(self.main.ed_lvo.text().replace(',', '.'))
            Svo = float(self.main.ed_Svo.text().replace(',', '.'))

            # Относительная толщина горизонт и вертикал оперения
            global cgo_, cvo_
            cvo_ = cgo_ = float(
                '%.3f' % (c_ - 0.01))  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! у всех разное число отнимается
            self.main.ed_cgo_.setText(str(cgo_))
            self.main.ed_cvo_.setText(str(cvo_))

            # Удлинение гор оперения
            global lgo, Sgo, lamdago
            lgo = float(self.main.ed_lgo.text().replace(',', '.'))
            Sgo = float(self.main.ed_Sgo.text().replace(',', '.'))
            lamdago = float('%.3f' % (lgo ** 2 / Sgo))
            self.main.ed_lamdago.setText(str(lamdago))

            global nvo, ngo
            ngo = float(self.main.ed_ngo.text().replace(',', '.'))
            nvo = float(self.main.ed_nvo.text().replace(',', '.'))

        except ValueError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Неправильный ввод данных.")
            msg.setWindowTitle("Ошибка")
            msg.setDetailedText("Вводить можно только цифры. Числа должны быть положительными.")
            msg.exec_()

        if permision_for_curve[0] and permision_for_curve[1] and permision_for_curve[2]:
            self.main.tabData.setTabEnabled(1, True)

    # ОПРЕДЕЛЕНИЕ ПЕРЕМЕННЫХ ПИЛОНА
    def CalculatePylon(self):

        try:
            global bp, cp_, Sp, npylon
            bp = float(self.main.ed_bp.text().replace(',', '.'))
            cp_ = float(self.main.ed_cp_.text().replace(',', '.'))
            Sp = float(self.main.ed_Sp.text().replace(',', '.'))
            npylon = float(self.main.ed_np.text().replace(',', '.'))

        except ValueError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Неправильный ввод данных.")
            msg.setWindowTitle("Ошибка")
            msg.setDetailedText("Вводить можно только цифры. Числа должны быть положительными.")
            msg.exec_()

        if permision_for_curve[0] and permision_for_curve[1] and permision_for_curve[2]:
            self.main.tabData.setTabEnabled(1, True)

    # РАСЧЕТ ДАННЫХ ФЮЗЕЛЯЖА
    def CalculateFuselage(self):

        try:
            # Диаметр миделя
            global Df, Smf
            Smf = float(self.main.ed_Smf.text().replace(',', '.'))
            Df = float('%.3f' % (math.sqrt(4 * Smf / math.pi)))
            self.main.ed_Df.setText(str(Df))

            # Удлинение
            global lamdaf, lf
            lf = float(self.main.ed_lf.text().replace(',', '.'))
            lamdaf = float('%.3f' % (lf / Df))
            self.main.ed_lamdaf.setText(str(lamdaf))

            # Смоченная поверхность
            global Ssm
            Ssm = float('%.3f' % (2.5 * lf * Df))
            self.main.ed_Ssm.setText(str(Ssm))

            # Удлинение носовой части
            global lnf, lamdanf
            lnf = float(self.main.ed_lnf.text().replace(',', '.'))
            lamdanf = float('%.3f' % (lnf / Df))
            self.main.ed_lamdanf.setText(str(lamdanf))

        except ValueError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Неправильный ввод данных.")
            msg.setWindowTitle("Ошибка")
            msg.setDetailedText("Вводить можно только цифры. Числа должны быть положительными.")
            msg.exec_()

        if permision_for_curve[0] and permision_for_curve[1] and permision_for_curve[2]:
            self.main.tabData.setTabEnabled(1, True)

    # РАСЧЕТ ДАННЫХ ГОНДОЛ ДВИГАТЕЛЯ И ШАССИ
    def CalculateGondola(self):
        global c_lamda_el_for_cxa

        try:
            # Удлинение гондола двигателя
            global lgd, Dgd, lamdagd
            lgd = float(self.main.ed_lgd.text().replace(',', '.'))
            Dgd = float(self.main.ed_Dgd.text().replace(',', '.'))
            lamdagd = float('%.3f' % (lgd / Dgd))
            self.main.ed_lamdagd.setText(str(lamdagd))

            # Удлинение смоченная поверхность гондола двигателя
            global Ssm_gd
            Ssm_gd = float('%.3f' % (2.5 * lgd * Dgd))
            self.main.ed_Ssmgd.setText(str(Ssm_gd))

            # Удлинение удлинение носовой части гондола двигателя
            global ln_gd, lamdan_gd
            ln_gd = float(self.main.ed_lngd.text().replace(',', '.'))
            lamdan_gd = float('%.3f' % (ln_gd / Dgd))
            self.main.ed_lamdangd.setText(str(lamdan_gd))

            # Удлинение гондола шасси
            global lgsh, Dgsh, lamdagsh
            lgsh = float(self.main.ed_lgsh.text().replace(',', '.'))
            Dgsh = float(self.main.ed_Dgsh.text().replace(',', '.'))
            lamdagsh = float('%.3f' % (lgsh / Dgsh))
            self.main.ed_lamdagsh.setText(str(lamdagsh))

            # Удлинение смоченная поверхность гондола шасси
            global Ssm_gsh
            Ssm_gsh = float('%.3f' % (2.5 * lgsh * Dgsh))
            self.main.ed_Ssmgsh.setText(str(Ssm_gsh))

            # Удлинение удлинение носовой части гондола шасси
            global ln_gsh, lamdan_gsh
            ln_gsh = float(self.main.ed_lngsh.text().replace(',', '.'))
            lamdan_gsh = float('%.3f' % (ln_gsh / Dgsh))
            self.main.ed_lamdangsh.setText(str(lamdan_gsh))

            global ngd, ngsh
            ngd = float(self.main.ed_ngd.text().replace(',', '.'))
            ngsh = float(self.main.ed_dsh.text().replace(',', '.'))

        except ValueError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Неправильный ввод данных.")
            msg.setWindowTitle("Ошибка")
            msg.setDetailedText("Вводить можно только цифры. Числа должны быть положительными.")
            msg.exec_()
        except ZeroDivisionError:
            lamdagd = lamdan_gd = lamdagsh = lamdan_gsh = Ssm_gd = Ssm_gsh = 0
            self.main.ed_lamdagd.setText(str(lamdagd))
            self.main.ed_lamdangd.setText(str(lamdan_gd))
            self.main.ed_Ssmgsh.setText(str(Ssm_gsh))
            self.main.ed_Ssmgd.setText(str(Ssm_gd))
            self.main.ed_lamdagsh.setText(str(lamdagsh))
            self.main.ed_lamdangsh.setText(str(lamdan_gsh))

            c_lamda_el_for_cxa.append(lamdagd)
            c_lamda_el_for_cxa.append(lamdagsh)

        if permision_for_curve[0] and permision_for_curve[1] and permision_for_curve[2]:
            self.main.tabData.setTabEnabled(1, True)

    # СОХРАНЕНИЕ ОБЩИХ ДАННЫХ
    def SafeCommonData(self):

        try:
            global Gvzl, V, number, P0, H, Dv, Fv
            Dv = float(self.main.ed_Dv.text().replace(',', '.'))
            Fv = float('%.3f' % (math.pi * Dv * Dv / 4))
            Gvzl = float(self.main.ed_Gvzl.text().replace(',', '.'))
            V = float(self.main.ed_V.text())
            number = float(self.main.ed_number.text().replace(',', '.'))
            P0 = float(self.main.ed_P0.text().replace(',', '.'))
            H = float(self.main.ed_H.text().replace(',', '.'))
            self.find_with_H(H)

            # Тип двигателей
            global type
            if self.main.radioButton_PD.isChecked():
                type = 'ТВД и ПД'
            elif self.main.radioButton_TRD.isChecked():
                type = 'ТРД'
            else:
                msg_ = QMessageBox()
                msg_.setIcon(QMessageBox.Warning)
                msg_.setText("Выберите тип двигателя.")
                msg_.setWindowTitle("Предупреждение")
                msg_.exec_()

            if type != '':
                global Gm
                Gm = self.findGm()

            global Kint, cxk_light
            if self.main.rb_circle.isChecked():
                Kint = self.request_Kint('Низкоплан с фюзеляжем круглого сечения')
            elif self.main.rb_oval.isChecked():
                Kint = self.request_Kint('Низкоплан с фюзеляжем овального сечения')
            elif self.main.rb_rectangle.isChecked():
                Kint = self.request_Kint('Низкоплан с фюзеляжем прямоугольного сечения')
            elif self.main.rb_middle.isChecked():
                Kint = self.request_Kint('Среднеплан')
            elif self.main.rb_high.isChecked():
                Kint = self.request_Kint('Высокоплан')

            if self.main.rb_1.isChecked():
                cxk_light = self.request_cxk('Фонарь с плоской передней стенкой')
            elif self.main.rb_2.isChecked():
                cxk_light = self.request_cxk('Плавный переход задней части фонаря в фюзеляж')
            elif self.main.rb_3.isChecked():
                cxk_light = self.request_cxk('Фонарь обтекаемой формы с плоскими передними стенками')
            elif self.main.rb_no.isChecked():
                cxk_light = self.request_cxk('Отсутствует')

            global nlight
            nlight = float(self.main.ed_nlight.text())

            permision_for_curve[2] = True
        except ValueError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Неправильный ввод данных.")
            msg.setWindowTitle("Ошибка")
            msg.setDetailedText("Вводить можно только цифры. Числа должны быть положительными.")
            msg.exec_()

        if permision_for_curve[0] and permision_for_curve[1] and permision_for_curve[2]:
            self.main.tabData.setTabEnabled(1, True)

    # РАСЧЕТ И ПОСТРОЕНИЕ КРИВОЙ ЗАВИСИМОСТИ Мкр
    def MakeMkr(self):
        self.main.tabWidget.setCurrentIndex(0)
        self.main.buHelp.setVisible(True)
        self.iconbutton(self.main.buMkr, self.button_curve)

        # ЗАПОЛНЕНИЕ МАССИВОВ ДАННЫМИ
        global linear_size, c_lamda_el_for_cxa, Sk_el_for_cxa, n_el_for_cxa
        linear_size = [b, bgo, bvo, bp, lf, lgd, lgsh, 0]  # фонарь!=0
        c_lamda_el_for_cxa = [c_, cgo_, cvo_, cp_, lamdaf, lamdagd, lamdagsh, 0]
        Sk_el_for_cxa = [S, Sgo, Svo, Sp, Ssm * 0.5, Ssm_gd * 0.5, Ssm_gsh * 0.5, 0]
        n_el_for_cxa = [1, ngo, nvo, npylon, 1, ngd, ngsh, nlight]

        # Расчет координат вспомогательной прямой
        arr_cya = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
        arr_Mkr = []
        for cya in arr_cya:
            expression = 1 - 0.445 * math.pow(lamdaef - 1, 1 / 9) * (0.175 + 3.25 * c_) * (
                    math.cos(x_degree * math.pi / 180) + (0.365 * cya ** 2) / math.cos(
                x_degree * math.pi / 180) ** 5)
            arr_Mkr.append(float('%.3f' % expression))

        global list_Mkr
        list_Mkr = arr_Mkr.copy()

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
        #ax.set_title('Кривая зависимости Мкр = f(cya)', loc='right', pad=5, fontsize=11)

        tck, u = interpolate.splprep([arr_cya, arr_Mkr], s=0)
        xnew, ynew = interpolate.splev(np.linspace(0, 1, 100), tck, der=0)

        ax.plot(arr_cya, arr_Mkr, '.', xnew, ynew, color='k')
        ax.plot(cya_rasch, Mrasch, marker='.', color='navy')

        ax.text(cya_rasch, Mrasch, '  A(Мрасч;Суа расч)', rotation=0, fontsize=7)

        ax.legend(['Координаты', 'Мкр = f(cya)', ], loc='lower left')

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_ylabel('$\it{Cya}$', loc='top', rotation=0)
        ax.set_xlabel('$\it{Mкр}$', loc='right', fontsize=11)

        self.figure.tight_layout()
        self.canvas.draw()


    # ПОСТРОЕНИЕ ВСПОМОГАТЕЛЬНОЙ КРИВОЙ cya = f(a)
    def MakeHelp(self):
        self.main.buUp.setVisible(True)
        self.iconbutton(self.main.buHelp, self.button_curve)
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
        self.find_Cyamaxprof()
        Cyamax = float('%.3f' % (Cyamaxprof * Kn * (1 + math.cos(x_degree * math.pi / 180)) / 2))
        k = cya_py2 / (alfa_px2 - a0)
        b = (-1) * k * a0
        px4 = float('%.3f' % ((Cyamax - b) / k))

        print('Kn = ' + str(Kn))
        print('Cyamax = ' + str(Cyamax))
        # Точка 3 - (x, 0.85 * суа_max)
        cya_py3 = float('%.3f' % (0.85 * Cyamax))
        px3 = float('%.3f' % ((cya_py3 - b) / k))

        # Точка 5 - (deltaalfa ,суа_max)
        deltaalfa = 2  # !!! произвольно
        px5 = px4 + deltaalfa
        py5 = Cyamax

        # заполнение списков для последующего использования во вспомогательной поляре
        global a_list_help, cya_list_help
        a_list_help.clear()
        cya_list_help.clear()
        a_list_help.append(a0)
        cya_list_help.append(0)
        a = 1  # !!!!!
        while px5 - a > 3:
            a_list_help.append(a)
            cya_list_help.append(float('%.3f' % (k*a+b)))
            a += 3
        a_list_help.append(px5)
        cya_list_help.append(Cyamax)

        # Отрисовка
        arrX_ = [a0, alfa_px2, px3, px4]
        arrY_ = [0, cya_py2, cya_py3, Cyamax]
        ax.plot(arrX_, arrY_, '--', color='k')
        arrX = [a0, alfa_px2, px3]
        arrY = [0, cya_py2, cya_py3]
        ax.plot(arrX, arrY, color='k')

        px = (px3 + px4) / 2
        py = (cya_py3 + Cyamax) / 2
        # Точка 6 - вспомогательная для дуги
        px6 = 2 * px5 - px3
        py6 = cya_py3

        arr_intr_X = [px3, px, px5, px6]
        arr_intr_Y = [cya_py3, py, py5, py6]
        tck, u = interpolate.splprep([arr_intr_X, arr_intr_Y], k=2, s=0)
        xnew, ynew = interpolate.splev(np.linspace(0, 1, 100), tck, der=0)
        ax.plot(arr_intr_X, arr_intr_Y, ' ', xnew, ynew, color='k')

        ax.plot(a0, 0, marker='o')
        ax.plot(alfa_px2, cya_py2, marker='o')
        ax.plot(px3, cya_py3, marker='o')
        ax.plot(px4, Cyamax, marker='o')
        ax.plot(px5, py5, marker='o')

        ax.legend(loc='lower right')
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_ylabel('$\it{Cya}$', loc = 'top', rotation=0)
        ax.set_xlabel('$\it{α, °}$', loc = 'right', fontsize=11)

        self.fhelp.tight_layout()
        self.chelp.draw()

        # Отображение в окне
        self.main.la_1_help.setText(str(a0) + '; ' + str(0))
        self.main.la_2_help.setText(str(alfa_px2) + '; ' + str(cya_py2))
        self.main.la_3_help.setText(str(px3) + '; ' + str(cya_py3))
        self.main.la_4_help.setText(str(px4) + '; ' + str(Cyamax))
        self.main.la_5_help.setText(str(px5) + '; ' + str(Cyamax))

        self.main.la_Re_help.setText(str(Re))
        self.main.la_Vmin_help.setText(str(float('%.3f' % Vmin)))
        self.main.la_Cyamaxprof_help.setText(str(Cyamaxprof))
        self.main.la_Kn_help.setText(str(Kn))


        # x=np.array( [px3,px5])
        # y = np.array([cya_py3, Cyamax])
        # x_new = np.linspace(x.min(), x.max(), 500)
        # f = interpolate.interp1d(x, y, kind='quadratic')
        # y_smooth = f(x_new)
        # ax.plot(x_new, y_smooth)

       # ax.set_title('Вспомогательная кривая Cya = f(a)', loc='left', pad=5, fontsize=11)


    # ПОИСК КОЭФФИЦИЕНТА ОТ ТИПА ЗАКРЫЛОК
    def find_zak(self, Flap_type):
        global dCyamax, dCxomax
        Sql_request = 'SELECT * FROM Закрылки WHERE Тип_механизации = %s' % '"' + Flap_type + '"'
        self.cursor.execute(Sql_request)
        cur = self.cursor.fetchone()
        dCyamax = float(cur[2])
        dCxomax = float(cur[3])

    # ПОСТРОЕНИЕ ВЗЛЕТНОЙ КРИВОЙ (С УЧЕТОМ И БЕЗ УЧЕТА ВЛИЯНИЯ ЭКРАНА ЗЕМЛИ)
    def MakeUp(self):
        self.main.tabWidget.setCurrentIndex(2)
        self.main.buDown.setVisible(True)
        self.iconbutton(self.main.buUp, self.button_curve)

        # 1) Без учета влияния экрана земли

        # Определение переменных по графикам da0_vzl
        self.find_zak(Flap_type)
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
        if Dv != 0:
            W = Vmin/2 + math.sqrt(math.pow(Vmin/2, 2) + (4*Gvzl)/(math.pi*n*p_zero*10*Dv*Dv))
            dCya_obd = -caya*(-1.5+a0)*math.pow(W/Vmin, 2)*Sobd_
            da0_obd = (1.5+a0)*math.pow(W/Vmin, 2)*Sobd_
        else:
            dCya_obd = 0
            da0_obd = 0


        # Максимальный коэф подъемной силы при взлете
        global Cyamax_vzl
        Cyamax_vzl = float('%.3f' % (Cyamax + dCyamax_pr + dCyamax_zak_vzl+dCya_obd)) #+dCya_obd
        a0_vzl = float('%.3f' % (a0 + (da0_vzl+da0_obd) * 180 / math.pi))  # +da0_obd

        # Точка
        cya = float('%.3f' % (caya * (5 - a0_vzl)))
        k = cya / (5 - a0_vzl)
        b = (-1) * k * a0_vzl
        px3_max = float('%.3f' % ((Cyamax_vzl - b) / k))

        # Отображение найденных переменных
        self.main.la_dCyamaxpr_Up.setText(str(dCyamax_pr))
        self.main.la_dCyamaxzakvzl_Up.setText(str(dCyamax_zak_vzl))
        self.main.la_dCyaobd_Up.setText(str(dCya_obd ))  # найти переменную с винтами
        self.main.la_Cyamax_Up.setText(str(Cyamax))
        self.main.la_Cyamaxvzl_Up.setText(str(Cyamax_vzl))
        self.main.la_dCyamax_Up.setText(str(dCyamax))
        self.main.la_da0vzl_Up.setText(str(da0_vzl))
        self.main.la_da0obd_Up.setText(str(da0_obd))  # найти переменную с винтами
        self.main.la_a0_Up.setText(str(a0))
        self.main.la_a0vzl_Up.setText(str(a0_vzl))
        self.main.la_Cya_Up.setText(str(cya))

        # Отрисовка
        self.fUp.clear()
        ax = self.fUp.add_subplot(111)

        # Вспомогательные точки
        px1 = (5 + 8 * (px3_max - 5) / 10)
        py1 = k * px1 + b

        px2 = px3_max + 2
        py2 = Cyamax_vzl

        px3 = 2 * px2 - px1
        py3 = py1

        points_a = [a0_vzl, 5, px1]
        points_Cya = [0, cya, py1]
        arr_intr_X = [px1, px2, px3]
        arr_intr_Y = [py1, py2, py3]

        tck, u = interpolate.splprep([arr_intr_X, arr_intr_Y], k=2)
        xnew, ynew = interpolate.splev(np.linspace(0, 1, 100), tck, der=0)
        ax.plot(arr_intr_X, arr_intr_Y, ' ', xnew, ynew, color='k')

        ax.plot(points_a, points_Cya, marker=' ', color='k')
        ax.plot(px2, Cyamax_vzl, marker='.', color='purple')

        # заполнение списков для взлетной кривой
        global a_list_up, cya_list_up
        a_list_up.clear()
        cya_list_up.clear()
        a_list_up.append(a0_vzl)
        cya_list_up.append(0)
        a = 1  # !!!!!
        while px2 - a > 3:
            angle = round(a0_vzl+a)
            a_list_up.append(angle)
            cya_list_up.append(float('%.3f' % (k * angle + b)))
            a += 3
        a_list_up.append(px2)
        cya_list_up.append(Cyamax_vzl)

        # 2) С учетом влияния экрана земли
        # Приращение КПС, вызванный экранным влиянияем земли
        dCyamax_zak_vzl_scrin = float('%.3f' % (-1 * 0.115 * math.exp(-0.5 * h / bsrzak) * Cyamax_vzl))

        # КПС, вызванный экранным влиянияем земли
        global Cyamax_vzl_scrin, lamdaef_scrin
        Cyamax_vzl_scrin = float('%.3f' % (Cyamax_vzl + dCyamax_zak_vzl_scrin))

        # Фиктивное удлинение крыла, учитывающее влияние экрана земли
        lamdaef_scrin = float('%.3f' % ((lamdaef / 2.23) * ((math.pi * l) / (8 * hvzl) + 2)))

        # Производная с учетом влияния экрана земли
        expression = (2 * math.pi * lamdaef_scrin * math.cos(x_degree * math.pi / 180)) / (
                57.3 * (lamdaef_scrin + 2 * math.cos(x_degree * math.pi / 180)))
        caya_scrin = float('%.3f' % expression)

        # Точка
        cya_s = float('%.3f' % (caya_scrin * (5 - a0_vzl)))
        k_s = cya_s / (5 - a0_vzl)
        b_s = (-1) * k_s * a0_vzl
        px3_max_s = float('%.3f' % ((Cyamax_vzl_scrin - b_s) / k_s))

        # Отображение найденных переменных
        self.main.la_dCyamaxvzl_scrin_Up.setText(str(dCyamax_zak_vzl_scrin))
        self.main.la_Cyamaxvzl_scrin_Up.setText(str(Cyamax_vzl_scrin))
        self.main.la_Caya_scrin_Up.setText(str(caya_scrin))
        self.main.la_lamda_scrin_Up.setText(str(lamdaef_scrin))
        self.main.la_Cya_scrin_Up.setText(str(cya_s))

        # Отрисовка
        px1_s = (5 + 8 * (px3_max_s - 5) / 10)
        py1_s = k_s * px1_s + b_s

        px2_s = px3_max_s + 2
        py2_s = Cyamax_vzl_scrin

        px3_s = 2 * px2_s - px1_s
        py3_s = py1_s

        points_a_s = [a0_vzl, 5, px1_s]
        points_Cya_s = [0, cya_s, py1_s]
        arr_intr_X_s = [px1_s, px2_s, px3_s]
        arr_intr_Y_s = [py1_s, py2_s, py3_s]

        tck, u = interpolate.splprep([arr_intr_X_s, arr_intr_Y_s], k=2)
        xnew_s, ynew_s = interpolate.splev(np.linspace(0, 1, 100), tck, der=0)
        ax.plot(arr_intr_X_s, arr_intr_Y_s, ' ', xnew_s, ynew_s, color='tab:blue')

        ax.plot(points_a_s, points_Cya_s, marker=' ', color='tab:blue')
        ax.plot(px2_s, Cyamax_vzl_scrin, marker='.', color='k')

        #ax.set_title('Взлетные кривые Cya = f(a)', loc='right', pad=5, fontsize=11)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_ylabel('$\it{Cya}$', loc='top', rotation=0)
        ax.set_xlabel('$\it{α, °}$', loc='right', fontsize=11)
        self.fUp.tight_layout()
        self.cUp.draw()

        # заполнение списков для взлетной кривой
        global a_list_up_scrin, cya_list_up_scrin
        a_list_up_scrin.clear()
        cya_list_up_scrin.clear()
        a_list_up_scrin.append(a0_vzl)
        cya_list_up_scrin.append(0)
        a = 1  # !!!!!
        while px2_s - a > 3:
            angle = round(a0_vzl+a)
            a_list_up_scrin.append(angle)
            cya_list_up_scrin.append(float('%.3f' % (k * angle + b)))
            a += 3
        a_list_up_scrin.append(px2_s)
        cya_list_up_scrin.append(Cyamax_vzl_scrin)

    # ПОСТРОЕНИЕ ПОСАДОЧНЫХ КРИВЫХ (С УЧЕТОМ И БЕЗ УЧЕТА ВЛИЯНИЯ ЭКРАНА ЗЕМЛИ)
    def MakeDown(self):
        self.main.tabWidget.setCurrentIndex(3)
        self.main.buCre.setVisible(True)
        self.iconbutton(self.main.buDown, self.button_curve)

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
        global Cya_max_pos
        Cya_max_pos = float('%.3f' % (Cyamax + dCyamax_pr + dCya_max_zak_pos))
        a0_pos = float('%.3f' % (a0 + da0_pos * 180 / math.pi))

        # Точка
        cya = float('%.3f' % (caya * (5 - a0_pos)))
        k = cya / (5 - a0_pos)
        b = -1 * k * a0_pos
        px3_max = float('%.3f' % ((Cya_max_pos - b) / k))

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

        px1 = (5 + 8 * (px3_max - 5) / 10)
        py1 = k * px1 + b

        px2 = px3_max + 2
        py2 = Cya_max_pos

        px3 = 2 * px2 - px1
        py3 = py1

        points_a = [a0_pos, 5, px1]
        points_Cya = [0, cya, py1]
        arr_intr_X = [px1, px2, px3]
        arr_intr_Y = [py1, py2, py3]

        tck, u = interpolate.splprep([arr_intr_X, arr_intr_Y], k=2)
        xnew, ynew = interpolate.splev(np.linspace(0, 1, 100), tck, der=0)
        ax.plot(arr_intr_X, arr_intr_Y, ' ', xnew, ynew, color='k')

        ax.plot(points_a, points_Cya, marker=' ', color='k')
        ax.plot(px2, Cya_max_pos, marker='.', color='purple')

        #ax.set_title('Посадочные кривые Cya = f(a)', loc='right', pad=5, fontsize=11)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_ylabel('$\it{Cya}$', loc='top', rotation=0)
        ax.set_xlabel('$\it{α, °}$', loc='right', fontsize=11)
        self.fDown.tight_layout()

        # заполнение списков для взлетной кривой
        global a_list_down, cya_list_down
        a_list_down.clear()
        cya_list_down.clear()
        a_list_down.append(a0_pos)
        cya_list_down.append(0)
        a = 1  # !!!!!
        while px2 - a > 3:
            angle = round((a0_pos+a))
            a_list_down.append(a)
            cya_list_down.append(float('%.3f' % (k * a + b)))
            a += 3
        a_list_down.append(px2)
        cya_list_down.append(Cya_max_pos)

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
        global Cya_max_pos_scrin, lamdaef_down_scrin
        Cya_max_pos_scrin = float('%.3f' % (Cya_max_pos + dCya_max_zak_pos_scrin))
        lamdaef_down_scrin=lamda_scrin

        #   Точка
        cya_scrin = float('%.3f' % (caya_scrin * (5 - a0_pos)))
        k_s = cya_scrin / (5 - a0_pos)
        b_s = -1 * k_s * a0_pos
        px3_max_s = float('%.3f' % ((Cya_max_pos_scrin - b_s) / k_s))

        # Отображение найденных переменных
        self.main.la_dCyamaxpos_scrin_Down.setText(str(dCya_max_zak_pos_scrin))
        self.main.la_Cyamaxpos_scrin_Down.setText(str(Cya_max_pos_scrin))
        self.main.la_Caya_scrin_Down.setText(str(caya_scrin))
        self.main.la_lamda_scrin_Down.setText(str(lamda_scrin))
        self.main.la_Cya_scrin_Down.setText(str(cya_scrin))

        # Отрисовка
        px1_s = (5 + 8 * (px3_max_s - 5) / 10)
        py1_s = k_s * px1_s + b_s

        px2_s = px3_max_s + 2
        py2_s = Cya_max_pos_scrin

        px3_s = 2 * px2_s - px1_s
        py3_s = py1_s

        points_a_s = [a0_pos, 5, px1_s]
        points_Cya_s = [0, cya_scrin, py1_s]
        arr_intr_X_s = [px1_s, px2_s, px3_s]
        arr_intr_Y_s = [py1_s, py2_s, py3_s]

        tck, u = interpolate.splprep([arr_intr_X_s, arr_intr_Y_s], k=2)
        xnew, ynew = interpolate.splev(np.linspace(0, 1, 100), tck, der=0)
        ax.plot(arr_intr_X_s, arr_intr_Y_s, ' ', xnew, ynew, color='tab:blue')

        ax.plot(points_a_s, points_Cya_s, marker=' ', color='tab:blue')
        ax.plot(px2_s, Cya_max_pos_scrin, marker='.', color='k')
        self.cDown.draw()

        # заполнение списков для взлетной кривой
        global a_list_down_scrin, cya_list_down_scrin
        a_list_down_scrin.clear()
        cya_list_down_scrin.clear()
        a_list_down_scrin.append(a0_pos)
        cya_list_down_scrin.append(0)
        a = 1  # !!!!!
        while px2_s - a > 3:
            angle =round(a0_pos+a)
            a_list_down_scrin.append(a)
            cya_list_down_scrin.append(float('%.3f' % (k * a + b)))
            a += 3
        a_list_down_scrin.append(px2_s)
        cya_list_down_scrin.append(Cya_max_pos_scrin)

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
        self.iconbutton(self.main.buCre, self.button_curve)

        list_M = self.func_type(type)
        list_caya_szh = []
        list_cya = []
        for M in list_M:
            caya_szh = caya / math.sqrt(1 - M ** 2)
            list_caya_szh.append(float('%.3f' % caya_szh))

            cya = caya_szh * (5 - a0)
            list_cya.append(float('%.3f' % cya))

        #  Построение
        self.fCruise.clear()
        ax = self.fCruise.add_subplot(111)
        for cya in list_cya:
            point_alfa = [a0, 5]
            point_cya = [0, cya]
            ax.plot(point_alfa, point_cya, color='k', linewidth=1)
            ax.annotate('M = '+ str(list_M[list_cya.index(cya)]), xy=(5, cya), xytext = (5,5),  textcoords='offset points')


        ax.vlines(5, 0, list_cya[-1], color='k', linewidth=1, linestyle='--')
        #ax.set_title('Крейсерские кривые Суа = f(a)', loc='left', pad=5, fontsize=11)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_ylabel('$\it{Cya}$', loc='top', rotation=0)
        ax.set_xlabel('$\it{α, °}$', loc='right', fontsize=11)
        self.fCruise.tight_layout()
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

        self.main.tabData.setTabEnabled(2, True)
        #self.MakeHelpPolyr()
        self.cCruise.draw()

    # ВСПОМОГАТЕЛЬНАЯ ПОЛЯРА
    def MakeHelpPolyr(self):
        self.main.tabPolyr.setCurrentIndex(0)
        print('ВСПОМОГАТЕЛЬНАЯ ПОЛЯРА')

        # РАСЧЕТ КОЭФФИЦИЕНТА ПРОФИЛЬНОГО СОПРОТИВЛЕНИЯ
        Vmin_pol = float('%.3f' % (math.sqrt((2 * Gpol * g) / (p_zero * S * Cyamax))))
        # print('Vmin_pol = ' + str(Vmin_pol))
        M = Vmin_pol/340.294 # ЧЕ ЗА КОНСТАНТА ???????????
        delta = self.call_delta(lamdaef, n)

        print('Кинт = ' + str(Kint))
        print('cxk = ' + str(cxk_light))

        global xtau_el_for_cxa
        Re_el_for_cxa = []
        xtau_el_for_cxa = []
        cf_el_for_cxa = []
        nc_el_for_cxa = []
        nm_el_for_cxa = []
        nint_el_for_cxa = []
        cxk_el_for_cxa = []
        chislitel_el_for_cxa = []

        for el in linear_size:
            index = linear_size.index(el)
            # число Рейнольдса
            Re_el = float('%.3f' % ((float(Vmin_pol) * float(el)) / (v_zero * math.pow(10, 6))))  # степень 10^6
            Re_el_for_cxa.append(Re_el)
            # точка перехода
            if index == 0:
                xtau_el_for_cxa.append(xtau_)
                nint_el_for_cxa.append(float('%.3f' % (1 - Kint * Sf_)))  # nинт для крыла
            else:
                xtau_el_for_cxa.append(0)
            if el != 0:
                # коэф сопротивления плоской пластине
                cf_el_for_cxa.append(self.find_2cf(xtau_el_for_cxa[index], Re_el))
                # коэф nМ
                nm_el_for_cxa.append(1)  #    ВСТАВИТЬ ФУНКЦИЮ
                # коэф nc
                if index < 4:
                    nc_el_for_cxa.append(self.find_nc_wing(xtau_el_for_cxa[index], c_lamda_el_for_cxa[index]))
                else:
                    nc_el_for_cxa.append(self.find_nc_body_rotate(c_lamda_el_for_cxa[index]))
                # коэф nинт
                if index != 0:
                    nint_el_for_cxa.append(1)
                # коэф cxk
                cxk = cf_el_for_cxa[index] * nc_el_for_cxa[index] * nm_el_for_cxa[index] * nint_el_for_cxa[index]
                cxk_el_for_cxa.append(float('%.5f' % cxk))
            else:
                nc_el_for_cxa.append(0)
                cf_el_for_cxa.append(0)
                nm_el_for_cxa.append(0)
                nint_el_for_cxa.append(0)
                cxk_el_for_cxa.append(0)

        global S_proiz, cxo
        for el in Sk_el_for_cxa:
            i = Sk_el_for_cxa.index(el)
            chislitel = n_el_for_cxa[i] * cxk_el_for_cxa[i] * el
            chislitel_el_for_cxa.append(float('%.5f' % chislitel))
            S_proiz.append(float('%.5f' % (n_el_for_cxa[i] * nc_el_for_cxa[i]*nint_el_for_cxa[i]*el)))

        cxo = float('%.5f' % (sum(chislitel_el_for_cxa) * 1.04 / S))

        th = ['Крыло', 'Горизонтальное оперение', 'Вертикальное оперение', 'Пилон', 'Фюзеляж',
              'Гондола двигателя', 'Гондола шасси', 'Фонарь, кабины пилотов']
        td = ['Линейный размер', 'Re', 'xt', '2cf', 'c_, lamda', 'nc',
              'nM', 'nинт', 'cxk', 'Sk', 'n', 'n*cxk*ck*Sk']

        table = PrettyTable(th)

        table.add_row(linear_size)
        table.add_row(Re_el_for_cxa)
        table.add_row(xtau_el_for_cxa)
        table.add_row(cf_el_for_cxa)
        table.add_row(c_lamda_el_for_cxa)
        table.add_row(nc_el_for_cxa)
        table.add_row(nm_el_for_cxa)
        table.add_row(nint_el_for_cxa)
        table.add_row(cxk_el_for_cxa)
        table.add_row(Sk_el_for_cxa)
        table.add_row(n_el_for_cxa)
        table.add_row(chislitel_el_for_cxa)
        table.add_column('Расчетная величина', td)

        print(table)  # Печатаем таблицу
        print('cxo = ' + str(cxo))



        # Приращение коэффициента профильного сопротивления
        cya__list = []
        dCxp_list = []
        # Коэффициент вихревого индуктивного сопротивления самолета
        Cxi_list = []
        # Коэффициент лобового сопротивления
        Cxa_list=[]
        self.fP_Help.clear()
        ax = self.fP_Help.add_subplot()
        kmax=0

        for el in cya_list_help:
            # Отношение КПС к максимальному КПС
            cya_ = el/Cyamax
            cya__list.append(float('%.4f' % (cya_)))
            # Приращение коэффициента профильного сопротивления
            exp_dCxp = math.pow(cya_, 4)*(1-math.exp(-0.1*math.pow((cya_ - 0.4), 2)))
            dCxp_list.append(float('%.4f' % exp_dCxp))
            # Коэффициент вихревого индуктивного сопротивления
            exp_Cxi = ((el*el)/(math.pi*lamdaef))*((1+delta)/math.sqrt(1-M*M))
            Cxi_list.append(float('%.4f' % exp_Cxi))
            # Коэффициент лобового сопротивления
            Cxa_list.append(float('%.4f' % (cxo+exp_dCxp+exp_Cxi)))
        # Отрисовка с помощью интерполяции
        tck, u = interpolate.splprep([Cxa_list, cya_list_help], s=0)
        xnew, ynew = interpolate.splev(np.linspace(0, 1, 100), tck)
        ax.plot(Cxa_list, cya_list_help, '.', xnew, ynew, color='tab:blue')
        for x in xnew:  # построение касательной к поляре
            k = ynew[np.where(xnew == x)]/x
            if kmax < k:
                kmax = k
                xmax=x
        ax.plot(xmax, kmax*xmax, '.', [0, xmax*2], [0, kmax*xmax*2 ], linewidth = 1, color = 'crimson')


        # КОЛИЧЕТСВО ДВИГАТЕЛЕЙ ЭТО НУМЕР !!!!!!!!!

        table_coordinats = PrettyTable(a_list_help)
        table_coordinats.add_row(cya_list_help)
        table_coordinats.add_row(cya__list)
        table_coordinats.add_row(dCxp_list)
        table_coordinats.add_row(Cxi_list)
        table_coordinats.add_row(Cxa_list)

        # print(table_coordinats)

        self.main.la_Vminpol.setText(str(Vmin_pol))
        self.main.la_M_Vmin.setText(str(float('%.3f' % M)))


        index=0
        for i, j in zip(Cxa_list, cya_list_help):
            ax.annotate(str(a_list_help[index]), xy=(i, j))
            index +=1

        # point_x = [min(Cxa_list),min(Cxa_list)]
        # point_y = [0, max(cya_list_help)/2]
        # ax.plot(point_x, point_y, color='green')
        # ax.set_title('Вспомогательная поляра', loc='left', pad=5, fontsize=11)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_ylabel('$\it{Cya}$', loc='top', rotation=0)
        ax.set_xlabel('$\it{Cxa}$', loc='right', fontsize=11)
        self.fP_Help.tight_layout()
        self.cP_Help.draw()

        #self.MakeUpPolyr()

    # ВЗЛЕТНАЯ ПОЛЯРА
    def MakeUpPolyr(self):
        # print(dCxomax)
        # print(self.find_dCxo_zak(bzak_, deltavzl))
        # print(deltavzl)
        self.main.tabPolyr.setCurrentIndex(1)
        print()
        print("ВЗЛЕТНАЯ ПОЛЯРА ")

        # 1) без учета влияния экрана земли
        delta = self.call_delta(lamdaef, n)
        cya__list_up = []
        dCxp_list_up = []
        Cxi_list_up = []
        Cxa_list_up = []


        cxo_vzl =  cxo + 0.5*cxo + 10 * self.find_dCxo_zak(bzak_, deltavzl) * Sobzak_ * dCxomax
        print('cxo_vzl = '+ str(float('%.3f' % cxo_vzl)))
        Vvzl = math.sqrt((2*Gvzl*g)/(0.8 * p_zero * S * Cyamax_vzl)) #!!!!! почему с экраном ?
        print('V_vzl = '+ str(float('%.3f' % Vvzl)))
        Mvzl = Vvzl/340.294 # CONST
        print('Mvzl = '+ str(float('%.3f' % Mvzl)))

        for el in cya_list_up:
            #
            cya_ = el /Cyamax_vzl # какой суа макс нужен ??
            cya__list_up.append(float('%.4f' % (cya_)))
            #
            exp_dCxp = math.pow(cya_, 4) * (1 - math.exp(-0.1 * math.pow((cya_ - 0.4), 2)))
            dCxp_list_up.append(float('%.4f' % exp_dCxp))
            #
            exp_Cxi = ((el * el) / (math.pi * lamdaef)) * ((1 + delta) / math.sqrt(1 - Mvzl * Mvzl))
            Cxi_list_up.append(float('%.4f' % exp_Cxi))
            #
            Cxa_list_up.append(float('%.4f' % (cxo_vzl + exp_dCxp + exp_Cxi)))

        table_coordinats = PrettyTable(a_list_up)
        table_coordinats.add_row(cya_list_up)
        table_coordinats.add_row(cya__list_up)
        table_coordinats.add_row(dCxp_list_up)
        table_coordinats.add_row(Cxi_list_up)
        table_coordinats.add_row(Cxa_list_up)
        # print(table_coordinats)

        # 1) c учетом влияния экрана земли
        delta = self.call_delta(lamdaef_scrin, n)
        cya__list_up_scrin = []
        dCxp_list_up_scrin = []
        Cxi_list_up_scrin = []
        Cxa_list_up_scrin = []

        Vvzl_scrin = math.sqrt((2 * Gvzl * g) / (0.8 * p_zero * S * Cyamax_vzl_scrin))  # !!!!! почему с экраном ?
        print('V_vzl_scrin = ' + str(float('%.3f' % Vvzl_scrin)))
        Mvzl_scrin = Vvzl_scrin / 340.294  # CONST
        print('Mvzl_scrin = ' + str(float('%.3f' % Mvzl_scrin)))

        for el in cya_list_up_scrin:
            #
            cya_ = el / Cyamax_vzl_scrin  # какой суа макс нужен ??
            cya__list_up_scrin.append(float('%.4f' % (cya_)))
            #
            exp_dCxp = math.pow(cya_, 4) * (1 - math.exp(-0.1 * math.pow((cya_ - 0.4), 2)))
            dCxp_list_up_scrin.append(float('%.4f' % exp_dCxp))
            #
            exp_Cxi = ((el * el) / (math.pi * lamdaef_scrin)) * ((1 + delta) / math.sqrt(1 - Mvzl_scrin * Mvzl_scrin))
            Cxi_list_up_scrin.append(float('%.4f' % exp_Cxi))
            #
            Cxa_list_up_scrin.append(float('%.4f' % (cxo_vzl + exp_dCxp + exp_Cxi)))

        table_coordinats_scrin = PrettyTable(a_list_up_scrin)
        table_coordinats_scrin.add_row(cya_list_up_scrin)
        table_coordinats_scrin.add_row(cya__list_up_scrin)
        table_coordinats_scrin.add_row(dCxp_list_up_scrin)
        table_coordinats_scrin.add_row(Cxi_list_up_scrin)
        table_coordinats_scrin.add_row(Cxa_list_up_scrin)
        # print(table_coordinats_scrin)

        # отрисовка
        self.fP_Up.clear()  # отчистка графика
        ax = self.fP_Up.add_subplot()
        # без экрана
        tck, u = interpolate.splprep([Cxa_list_up, cya_list_up], s=0)
        xnew, ynew = interpolate.splev(np.linspace(0, 1, 50), tck)
        ax.plot(Cxa_list_up, cya_list_up, '.', xnew, ynew, color='k')

        index=0
        for i, j in zip(Cxa_list_up, cya_list_up):
            ax.annotate(str(a_list_up[index]), xy=(i, j))
            index +=1

        # с экраном
        tck, u = interpolate.splprep([Cxa_list_up_scrin, cya_list_up_scrin], s=0)
        xnew, ynew = interpolate.splev(np.linspace(0, 1, 50), tck)
        ax.plot(Cxa_list_up_scrin, cya_list_up_scrin, '.', xnew, ynew, color='tab:blue')

        index = 0
        for i, j in zip(Cxa_list_up_scrin, cya_list_up_scrin):
            ax.annotate(str(a_list_up_scrin[index]), xy=(i, j))
            index += 1

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_ylabel('$\it{Cya}$', loc='top', rotation=0)
        ax.set_xlabel('$\it{Cxa}$', loc='right', fontsize=11)
        self.fP_Up.tight_layout()
        self.cP_Up.draw()

    # ПОСАДОЧНАЯ ПОЛЯРА
    def MakeDownPolyr(self):
        # print(dCxomax)
        # print(self.find_dCxo_zak(bzak_, deltavzl))
        # print(deltavzl)
        self.main.tabPolyr.setCurrentIndex(2)
        print()
        print("ПОСАДОЧНАЯ ПОЛЯРА ")

        # 1) без учета влияния экрана земли
        delta = self.call_delta(lamdaef, n)
        cya__list_down = []
        dCxp_list_down = []
        Cxi_list_down = []
        Cxa_list_down = []


        cxo_down =  cxo + 0.5*cxo + 10 * self.find_dCxo_zak(bzak_, deltapos) * Sobzak_ * dCxomax #!!!!!!!!!!!!!!!
        print('cxo_down = '+ str(float('%.3f' % cxo_down)))
        Vdown = math.sqrt((2*Gpol*g)/(0.8 * p_zero * S * Cya_max_pos)) #!!!!! почему с экраном ?
        print('V_down = '+ str(float('%.3f' % Vdown)))
        Mdown = Vdown/340.294 # CONST
        print('Mdown = '+ str(float('%.3f' % Mdown)))

        for el in cya_list_down:
            #
            cya_ = el /Cya_max_pos # какой суа макс нужен ??
            cya__list_down.append(float('%.4f' % (cya_)))
            #
            exp_dCxp = math.pow(cya_, 4) * (1 - math.exp(-0.1 * math.pow((cya_ - 0.4), 2)))
            dCxp_list_down.append(float('%.4f' % exp_dCxp))
            #
            exp_Cxi = ((el * el) / (math.pi * lamdaef)) * ((1 + delta) / math.sqrt(1 - Mdown * Mdown))
            Cxi_list_down.append(float('%.4f' % exp_Cxi))
            #
            Cxa_list_down.append(float('%.4f' % (cxo_down + exp_dCxp + exp_Cxi)))

        table_coordinats = PrettyTable(a_list_down)
        table_coordinats.add_row(cya_list_down)
        table_coordinats.add_row(cya__list_down)
        table_coordinats.add_row(dCxp_list_down)
        table_coordinats.add_row(Cxi_list_down)
        table_coordinats.add_row(Cxa_list_down)
        # print(table_coordinats)

        # 1) c учетом влияния экрана земли
        delta = self.call_delta(lamdaef_down_scrin, n)
        cya__list_down_scrin = []
        dCxp_list_down_scrin = []
        Cxi_list_down_scrin = []
        Cxa_list_down_scrin = []

        Vdown_scrin = math.sqrt((2 * Gpol * g) / (0.8 * p_zero * S * Cya_max_pos_scrin))  # !!!!! почему с экраном ?
        print('V_down_scrin = ' + str(float('%.3f' % Vdown_scrin)))
        Mdown_scrin = Vdown_scrin / 340.294  # CONST
        print('Mdown_scrin = ' + str(float('%.3f' % Mdown_scrin)))

        for el in cya_list_down_scrin:
            #
            cya_ = el / Cya_max_pos_scrin  # какой суа макс нужен ??
            cya__list_down_scrin.append(float('%.4f' % (cya_)))
            #
            exp_dCxp = math.pow(cya_, 4) * (1 - math.exp(-0.1 * math.pow((cya_ - 0.4), 2)))
            dCxp_list_down_scrin.append(float('%.4f' % exp_dCxp))
            #
            exp_Cxi = ((el * el) / (math.pi * lamdaef_down_scrin)) * ((1 + delta) / math.sqrt(1 - Mdown_scrin * Mdown_scrin))
            Cxi_list_down_scrin.append(float('%.4f' % exp_Cxi))
            #
            Cxa_list_down_scrin.append(float('%.4f' % (cxo_down + exp_dCxp + exp_Cxi)))

        table_coordinats_scrin = PrettyTable(a_list_down_scrin)
        table_coordinats_scrin.add_row(cya_list_down_scrin)
        table_coordinats_scrin.add_row(cya__list_down_scrin)
        table_coordinats_scrin.add_row(dCxp_list_down_scrin)
        table_coordinats_scrin.add_row(Cxi_list_down_scrin)
        table_coordinats_scrin.add_row(Cxa_list_down_scrin)
        # print(table_coordinats_scrin)

        # отрисовка
        self.fP_Down.clear()  # отчистка графика
        ax = self.fP_Down.add_subplot()
        # без экрана
        tck, u = interpolate.splprep([Cxa_list_down, cya_list_down], k=2, s = 0)
        xnew, ynew = interpolate.splev(np.linspace(0, 1, 100), tck)
        ax.plot(Cxa_list_down, cya_list_down, '.', xnew, ynew, color='k')

        index=0
        for i, j in zip(Cxa_list_down, cya_list_down):
            ax.annotate(str(a_list_down[index]), xy=(i, j))
            index +=1

        # с экраном
        tck, u = interpolate.splprep([Cxa_list_down_scrin, cya_list_down_scrin], k =2, s=0)
        xnew, ynew = interpolate.splev(np.linspace(0, 1, 100), tck)
        ax.plot(Cxa_list_down_scrin, cya_list_down_scrin, '.', xnew, ynew, color='tab:blue')

        index = 0
        for i, j in zip(Cxa_list_down_scrin, cya_list_down_scrin):
            ax.annotate(str(a_list_down_scrin[index]), xy=(i, j))
            index += 1

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_ylabel('$\it{Cya}$', loc='top', rotation=0)
        ax.set_xlabel('$\it{Cxa}$', loc='right', fontsize=11)
        self.fP_Down.tight_layout()
        self.cP_Down.draw()


    # КРЕЙСЕРСКИЕ ПОЛЯРЫ
    def MakeCruisePolyr(self):
        self.main.tabPolyr.setCurrentIndex(3)
        self.fP_Cre.clear()  # отчистка графика
        ax = self.fP_Cre.add_subplot()

        list_M = self.func_type(type)
        list_M.pop(0)
        print(list_M)
        list_Re = []
        list_Xak=[]
        list_2cf=[]
        list_nM = []
        list_cxo_cruise = []
        list_lamdan = c_lamda_el_for_cxa.copy()
        list_lamdan[4]=lamdanf
        list_lamdan[5]=lamdan_gd
        list_lamdan[6]=lamdan_gsh

        print ('КРЕЙСЕРСКИЕ ПОЛЯРЫ')
        for M in list_M:
            list_Re.clear()
            list_Xak.clear()
            list_2cf.clear()
            list_nM.clear()
            for el in linear_size:
                if el != 0:
                    index = linear_size.index(el)
                    el_c_lamda= list_lamdan[index]
                    xt = xtau_el_for_cxa[index]
                    if M == 0:
                        Re = (Vmin*el)/vH
                    else:
                        Re = (M * aH * el)/vH
                    list_Re.append(float('%.3f' % Re))
                    list_2cf.append(self.find_2cf(xt, Re))
                    if index < 4:
                        list_nM.append(self.call_nM_wing(el_c_lamda, M))
                    else:
                        list_nM.append(self.call_nM_body_rotation(el_c_lamda, M))
                    Xak = list_2cf[index] * S_proiz[index] * list_nM[index]
                    list_Xak.append(float('%.3f' % Xak))
                else:
                    list_Xak.append(0)
                    list_Re.append(0)
                    list_2cf.append(0)
                    list_nM.append(0)

            t = PrettyTable(['Крыло', "Гор оперение", "Вер оперение", "Пилон", "Фюзеляж", "ГД", "ГШ", "Фонарь"])
            t.add_row(list_Re)
            t.add_row(list_2cf)
            t.add_row(list_nM)
            t.add_row(list_Xak)
            print()
            print('M = '+ str(M))
            print(t)

            cxo_cruise = float('%.5f' % (sum(list_Xak) * 1.04 / S))
            list_cxo_cruise.append(cxo_cruise)
            print('cxo = ' + str(cxo_cruise))

            cos = math.cos(xc_degree)

        # Максимальный коэф волнового сопротивления при числе Маха =
        Mc_xvo_max = math.pow(cos,-1) * (1 + 0.4 * (math.pow(c_, 3/2) / math.pow(cos, 2/3)) *
                                                             (2 - lamdaef*math.pow(c_*cos*cos, 1/3)))
        cxvo_max = (2 * math.pi * lamdaef * c_ * c_ * cos) / (2 + lamdaef * math.pow(c_, 1/3) * math.pow(cos, 5/3))
        print('M max = ' + str(float('%.3f' % Mc_xvo_max)))
        print('C max = ' + str(float('%.3f' % cxvo_max)))


        # расчет координат поляр
        list_cya = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
        list_cxi=[]
        list_cxa = []
        list_cxvo = []
        list_cxvi = []
        delta = self.call_delta(lamdaef, n)

        for cya in list_cya:
            Mkr = list_Mkr[list_cya.index(cya)]
            list_cxi.clear()
            list_cxa.clear()
            list_cxvo.clear()
            list_cxvi.clear()
            for M in list_M:
                i = list_M.index(M)
                # коэффициент вихревого сопротивления
                cxi = math.pow(cya, 2)/(math.pi*lamdaef) * (1+delta)/math.sqrt(1-M*M)
                list_cxi.append(float('%.5f' % cxi))

                if type == 'ТРД':
                    if M > Mkr:
                        # составляющая коэф волнового сопротивления, не зависящая от cya
                        Am = (M - Mkr) / (Mc_xvo_max - Mkr)
                        cxvo = cxvo_max * math.pow(Am, 3) * (4 - 3 * Am)
                        list_cxvo.append(float('%.5f' % cxvo))
                        # коэф волнового сопротивления
                        cxvi = 25 * lamdaef * math.pow(c_, 1 / 3) * math.pow(M - Mkr, 3) * cxi
                        list_cxvi.append(float('%.5f' % cxvi))
                    else:
                        list_cxvo.append(0)
                        list_cxvi.append(0)
                    # КЛС
                    cxa = list_cxo_cruise[i] + list_cxi[i]+list_cxvo[i]+list_cxvi[i]
                    list_cxa.append(float('%.5f' % cxa))
                else:
                    # КЛС
                    cxa = list_cxo_cruise[i] + list_cxi[i]
                    list_cxa.append(float('%.5f' % cxa))
            if type == 'ТРД':
                t = PrettyTable()
                t.add_column("M", list_M)
                t.add_column("cxo",list_cxo_cruise)
                t.add_column( "cxi", list_cxi)
                t.add_column('cxvo', list_cxvo)
                t.add_column('cxvi', list_cxvi)
                t.add_column("cxa", list_cxa)
                print()
                print('cya = ' + str(cya))
                print('Mkr = ' + str(Mkr))
                print(t)
            else:
                t = PrettyTable()
                t.add_column("M",list_M)
                t.add_column("cxo",list_cxo_cruise)
                t.add_column("cxi",list_cxi)
                t.add_column("cxa", list_cxa)
                print()
                print('cya = ' + str(cya))
                print(t)

            # отрисовка
            # print(list_cxa)
            # y = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
            # tck, u = interpolate.splprep([list_cya, y], s=0, k=2)
            # xnew, ynew = interpolate.splev(np.linspace(0, 1, 50), tck)
            # ax.plot(list_cya, y, '.', xnew, ynew, color='tab:blue')

        # index = 0
        # for i, j in zip(Cxa_list_up_scrin, cya_list_up_scrin):
        #     ax.annotate(str(a_list_up_scrin[index]), xy=(i, j))
        #     index += 1

        # ax.spines["top"].set_visible(False)
        # ax.spines["right"].set_visible(False)
        # ax.set_ylabel('$\it{Cya}$', loc='top', rotation=0)
        # ax.set_xlabel('$\it{Cxa}$', loc='right', fontsize=11)
        # self.fP_Cre.tight_layout()

        list_H=[0, 3000, 6000, 9000, 12000]
        list_cya_pol = []
        # print(list_M)
        # print(H)
        # ph_rash = pH
        # ah_rash = aH
        Vmin_rash = math.sqrt((2*Gpol*g)/(0.85*pH*S*Cyamax))
        Mmin_rash = Vmin_rash / aH
        if type == "ТРД":
            for H_ in list_H:
                self.find_with_H(H_)
                list_cya_pol.clear()
                for M in list_M:
                    cya=0
                    if M != 0:
                        cya = (2*Gpol*g)/(pH*S*aH*aH*M*M)
                    else:
                        cya = (2 * Gpol * g) / (pH * S * aH*aH*Mmin_rash*Mmin_rash)
                    list_cya_pol.append(float('%.4f' % cya))

                t = PrettyTable(list_M)
                t.add_row(list_cya_pol)
                print()
                print('H = ' + str(H_))
                print(t)

        self.cP_Cre.draw()






if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    # window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение
