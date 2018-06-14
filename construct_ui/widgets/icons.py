# -*- coding: utf-8 -*-
from __future__ import absolute_import

from Qt import QtWidgets, QtCore, QtGui
from bands import channel

from construct_ui import resources
from construct_ui.utils import get_scale_factor
from construct_ui.styled_property import StyledProperty


class Icon(QtWidgets.QLabel):

    clicked = channel('clicked')
    right_clicked = channel('right_clicked')

    def __init__(self, icon, size=24, parent=None):
        super(Icon, self).__init__('', parent=parent)
        StyledProperty.init(self)
        self.setMouseTracking(True)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setPixmap(resources.qpixmap(icon))
        _size = size * get_scale_factor()
        self.size = QtCore.QSize(_size, _size)

    def minimumSizeHint(self):
        return self.size

    def mousePressEvent(self, event):
        if event.buttons() & QtCore.Qt.LeftButton:
            self.active = True
            self.clicked.send()
        elif event.buttons() & QtCore.Qt.RightButton:
            self.right_clicked.send()
        event.accept()

    def mouseReleaseEvent(self, event):

        self.active = False
        event.accept()
