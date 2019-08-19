# -*- coding: utf-8 -*-
from __future__ import absolute_import

from Qt import QtWidgets, QtCore, QtGui
from bands import channel

from construct_ui import resources
from construct_ui.utils import pix
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
        self.size = QtCore.QSize(pix(size), pix(size))

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


class ToggleIcon(QtWidgets.QLabel):

    clicked = channel('clicked')
    right_clicked = channel('right_clicked')
    toggled = channel('toggled')

    def __init__(self, disabled_icon, enabled_icon, size=24, parent=None):
        super(ToggleIcon, self).__init__('', parent=parent)
        StyledProperty.init(self)
        self.setMouseTracking(True)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.disabled_icon = resources.qpixmap(disabled_icon)
        self.enabled_icon = resources.qpixmap(enabled_icon)
        self.setPixmap(self.disabled_icon)
        self.size = QtCore.QSize(pix(size), pix(size))
        self.enabled = False

    def toggle(self):
        self.enabled = not self.enabled
        self.toggled.send(self.enabled)
        self.update_pixmap(self.enabled)

    def setEnabled(self, value):
        self.enabled = value
        self.update_pixmap(value)

    def update_pixmap(self, value=None):
        value = value or self.enabled
        if value:
            self.setPixmap(self.enabled_icon)
        else:
            self.setPixmap(self.disabled_icon)

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
        if self.active:
            self.toggle()
        self.active = False
        event.accept()


class DropDownIcon(ToggleIcon):

    def __init__(self, **kwargs):
        kwargs.setdefault('disabled_icon', ':/icons/right_arrow')
        kwargs.setdefault('enabled_icon', ':/icons/down_arrow')
        super(DropDownIcon, self).__init__(**kwargs)
