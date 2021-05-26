from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
# from PyQt5 import *

ON_COLOR = Qt.white
OFF_COLOR = Qt.black
ICON_SIZE = (48, 48)

class Led(QLabel):
    def __init__(self, parent):
        super().__init__(parent, )
        self._state = False
        self._pixmap = QPixmap(*ICON_SIZE)
        self.setOff()

    def setOn(self):
        self._pixmap.fill(ON_COLOR)
        self.setPixmap(self._pixmap)

    def setOff(self):
        self._pixmap.fill(OFF_COLOR)
        self.setPixmap(self._pixmap)

    def set(self, val):
        if val:
            self.setOn()
        else:
            self.setOff()
