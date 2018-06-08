# -*- coding: utf-8 -*-
from __future__ import absolute_import

from Qt import QtWidgets

from construct_ui.controls.control import Control
from construct_ui.controls.option_control import OptionControl


class StringControl(Control, QtWidgets.QLineEdit):

    def __init__(self, name, placeholder=None, default=None, parent=None):
        super(StringControl, self).__init__(name, default, parent)

    def create(self):
        self.textEdited.connect(self.send_changed)

    def get(self):
        return self.text()

    def set(self, value):
        return self.setText(value)


class StringOptionControl(OptionControl):
    pass
