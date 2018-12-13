# -*- coding: utf-8 -*-
from __future__ import absolute_import

from Qt import QtWidgets, QtCore

from construct_ui.utils import get_scale_factor
from construct_ui.widgets.icons import Icon
from construct_ui.widgets.labels import Label


class Header(QtWidgets.QWidget):

    def __init__(self, text, parent=None):
        super(Header, self).__init__(parent)

        self.menu = QtWidgets.QMenu(parent=self)
        self.menu_button = Icon(':/icons/menu', parent=self)
        self.menu_button.clicked.connect(self.show_menu)
        self.menu_button.setFixedSize(100, 100)
        self.menu_button.hide()
        self.header_label = Label(text)
        self.header_label.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.header_label.setFocusPolicy(QtCore.Qt.NoFocus)

        self.setMinimumHeight(48 * get_scale_factor())
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.menu_button)
        self.layout.addWidget(self.header_label)
        self.layout.addStretch(1)
        self.setLayout(self.layout)

    def show_menu(self):
        pos = QtCore.QPoint(0, self.menu_button.height())
        self.menu.popup(self.menu_button.mapToGlobal(pos))

    def add_menu_item(self, text, callback, icon=None):
        menu_item = QtWidgets.QAction(text, parent=self)
        menu_item.triggered.connect(callback)
        self.menu.addAction(menu_item)
        self.menu_button.show()

    def add_menu_callback(self, callback):
        self.menu.aboutToShow.connect(callback)
