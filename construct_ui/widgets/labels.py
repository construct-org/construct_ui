# -*- coding: utf-8 -*-
from __future__ import absolute_import
from Qt import  QtCore, QtWidgets
from construct_ui.properties import StyledProperty, init_properties


class Label(QtWidgets.QLabel):

    valid = StyledProperty('valid', True)

    def __init__(self, text, parent=None):
        super(Label, self).__init__(text, parent)
        init_properties(self)


class RightLabel(Label):

    def __init__(self, text, parent=None):
        super(RightLabel, self).__init__(text, parent)
        self.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)


class CenterLabel(Label):

    def __init__(self, text, parent=None):
        super(CenterLabel, self).__init__(text, parent)
        self.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
