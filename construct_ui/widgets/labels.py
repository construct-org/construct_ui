# -*- coding: utf-8 -*-
from __future__ import absolute_import

from Qt import QtCore, QtWidgets
from bands import channel

from construct_ui.styled_property import StyledProperty


class ClickableLabel(QtWidgets.QLabel):

    valid = StyledProperty('valid', True)
    clicked = channel('clicked')
    right_clicked = channel('right_clicked')

    def __init__(self, *args, **kwargs):
        super(ClickableLabel, self).__init__(*args, **kwargs)
        StyledProperty.init(self)
        self.setMouseTracking(True)

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


class Label(ClickableLabel):

    def __init__(self, *args, **kwargs):
        super(Label, self).__init__(*args, **kwargs)
        self.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)


class RightLabel(Label):

    def __init__(self, *args, **kwargs):
        super(RightLabel, self).__init__(*args, **kwargs)
        self.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)


class CenterLabel(Label):

    def __init__(self, *args, **kwargs):
        super(CenterLabel, self).__init__(*args, **kwargs)
        self.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
