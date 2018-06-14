# -*- coding: utf-8 -*-
from __future__ import absolute_import

from Qt import QtWidgets, QtCore

from construct_ui.controls.control import Control


class OptionControl(Control, QtWidgets.QComboBox):

    def __init__(self, name, options=None, default=None, parent=None):
        self.options = options
        super(OptionControl, self).__init__(name, default, parent)

    def create(self):
        self.activated.connect(self.send_changed)
        if self.options:
            self.set_options(self.options)

        self.setItemDelegate(QtWidgets.QStyledItemDelegate())

    def get_options(self, options):
        return self.options

    def set_options(self, options):
        self.clear()
        self.addItems(options)
        self.options = options

    def get_data(self):
        return self.itemData(
            self.currentIndex(),
            QtCore.Qt.UserRole
        )

    def get(self):
        return self.currentText()

    def set(self, value):
        self.setCurrentIndex(self.findText(value))
