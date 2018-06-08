# -*- coding: utf-8 -*-
from __future__ import absolute_import

from Qt import QtWidgets, QtCore

from construct_ui.widgets.buttons import IconButton
from construct_ui.widgets.labels import Label


class Header(QtWidgets.QWidget):

    def __init__(self, text, parent=None):
        super(Header, self).__init__(parent)

        self.menu = QtWidgets.QMenu(parent=self)
        self.menu_button = IconButton(parent=self)
        self.menu_button.clicked.connect(self.show_menu)
        self.header_label = Label(text, parent=self)

        self._layout = QtWidgets.QGridLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)

        self._layout.addWidget(0, 0, self.menu_button)
        self._layout.addWidget(0, 1, self.header_label)

    def show_menu(self):
        x = int(self.menu_button.width() * 0.5)
        y = self.menu_button.height()
        pos = self.menu_button.mapToGlobal(QtCore.QPoint(x, y))
        self.menu.popup(pos)

    def add_menu_item(self, text, callback, icon=None):
        pass

    def remove_menu_item(self):
        pass

    def add_menu_callback(self, callback):
        pass
