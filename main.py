# This Python file uses the following encoding: utf-8
import math
import os
import sys
import re
from math import *
from numpy import *

from PyQt5 import *
from PyQt5 import QtCore, QtGui, QtMultimedia, QtWidgets, uic
# from PyQt5.QtCore import *
from PyQt5.QtCore import QEvent, QFile, QLine, QLineF, QRect, QRectF, Qt, QTimer
# from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QWidget

DIR = os.path.dirname(__file__)
# LEDS = 4



class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        uic.loadUi(os.path.join(DIR, "main.ui"), self)
        self.setWindowTitle('Blinkus & Boopus')

        self.defaultProgram = "new = prev + 1\n\nif new >= 2 ** count:\n    new = 0\n\nreturn new"

        # with open(os.devnull, 'w') as f:
        #     # disable stdout
        #     oldstdout = sys.stdout
        #     sys.stdout = f

        #     import pygame

        #     # enable stdout
        #     sys.stdout = oldstdout

        # sys.stdout = TextIO() self.ou

        self.leds = self.grid.count()
        self.num = 0
        self.setToNum(self.num)
        self.lastSaveLoc = None
        self.lastSaveFolder = '~/'
        self.openVar = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.increment)
        self.timer.start(1000.0 / self.rate.value())

        self.rate.valueChanged.connect(self.resetTimer)
        self.rateDial.valueChanged.connect(self.resetTimer)

        self.code.textChanged.connect(self.resetStepFunc)

        self.resetButton.pressed.connect(self.reset)
        self.addButton.pressed.connect(self.add)
        self.resetFunc.pressed.connect(self.resetFunction)
        self.persistButton.pressed.connect(self.setPersist)

        self.save.triggered.connect(self._save)
        self.saveAs.triggered.connect(self._saveAs)
        self.load.triggered.connect(self._load)

        self.stepFunc = None
        self.resetStepFunc()
        self.stableStepFunc = self.stepFunc


    def print(self, txt):
        self.out.setText(txt)

    def setPersist(self):
        stat = 'self.openVar = ' + self.persistVal.text()
        try:
            _code = compile(self.persistVal.text(), 'Set Persist', 'eval')
        except Exception as err:
            print(err, 'in', stat)
        else:
            # print('setting persist to', stat)
            exec(stat)


    def resetFunction(self):
        self.code.setPlainText(self.defaultProgram)

    def _getFunc(self):
        return 'def inputCode(prev, count, rows, columns, rate, persist):\n    ' + re.sub(r'\n', r'\n    ', self.code.toPlainText()).strip() + ', rate, persist'
        # return 'def inputCode(self):\n    ' +
        # s = self.code.toPlainText()
        # for pattern, repl in {r'\n': r'\n    ', 'prev': 'self.num', 'count': 'self.leds', 'rows': 'self.grid.rowCount()', 'columns': 'self.grid.columnCount()', 'rate': 'self.rate', }.items():
            # s = re.sub(pattern, repl, s)


    def _saveAs(self):
        file = QFileDialog.getSaveFileName()[0]
        if len(file):
            with open(file, 'w') as f:
                f.write(self._getFunc())
            print('File Saved!')

    def _save(self):
        if self.lastSaveLoc:
            with open(self.lastSaveLoc, 'w') as f:
                f.write(self._getFunc())
            print('File Saved!')

    def _load(self):
        file = QFileDialog.getOpenFileName()[0]
        if len(file):
            with open(file, 'r') as f:
                self.code.setPlainText(f.read()[54:])

    def reset(self):
        self.num = self.resetVal.value()

    def add(self):
        self.num += self.addVal.value()

    def resetStepFunc(self):
        func = self._getFunc()
        try:
            _code = compile(func, 'Step Function', 'exec')
        except Exception as err:
            # print('executing this code:\n' + func)
            self.errorMsg.setPlainText(str(err))
            self.stepFunc = self.stableStepFunc
        else:
            # print('executing this code:\n' + func)
            exec(_code)

            #* THIS SHOULD WORK. WHY DOES THAT WORK BUT THIS DOESN'T???
            # self.stepFunc = inputCode
            self.stepFunc = locals()['inputCode']

            self.errorMsg.setPlainText('')

    def resetTimer(self, val):
        self.timer.start(int(1000.0 / val))
        self.rateDial.setValue(int(val))
        self.rate.setValue(val)

    def getLed(self, index):
        rows, columns = self.grid.rowCount(), self.grid.columnCount()
        # print(index % rows, math.floor(index / columns))
        tmp = self.grid.itemAtPosition(math.floor(index / columns), index % rows)
        if tmp:
            return tmp
        else:
            # return self.grid.itemAtPosition(rows, columns)
            print("FAILED")
            return self.grid.itemAt(index)

    def setToNum(self, num):
        for cnt, i in enumerate(reversed(f'{{:0{self.leds}b}}'.format(int(num)))):
            led = self.getLed(cnt).widget()
            if led:
                # print(f'setting led #{cnt} to {bool(int(i))}')
                led.set(int(i))
            else:
                return

    def increment(self):
        try:
            self.num, r, self.openVar = self.stepFunc(self.num, self.leds, self.grid.rowCount(), self.grid.columnCount(), self.rate.value(), self.openVar)
            self.resetTimer(r)
        except Exception as err:
            self.stepFunc = self.stableStepFunc
            self.errorMsg.setPlainText(str(err))
        else:
            self.stableStepFunc = self.stepFunc

        self.setToNum(self.num)
        # print(f'= {self.num}')



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    app.exec()
