# -*- coding: utf-8 -*-
from __future__ import absolute_import

from timeit import default_timer

from Qt import QtWidgets, QtCore
from bands import channel

from construct.compat import basestring
from construct_ui import resources


class IconButton(QtWidgets.QLabel):

    clicked = channel('clicked')
    double_clicked = channel('double_clicked')
    right_clicked = channel('right_clicked')

    def __init__(self, icon, parent=None):
        super(IconButton, self).__init__('', parent=parent)
        self.setPixmap(resources.qpixmap(icon))
        self.setProperty('iconbutton', True)

    def sizeHint(self):
        return QtCore.QSize(48, 48)

    def mousePressEvent(self, event):
        event.accept()

    def mouseMoveEvent(self, event):
        event.accept()

    def mouseReleaseEvent(self, event):
        event.accept()
