# -*- coding: utf-8 -*-
from __future__ import absolute_import

from Qt import QtCore, QtWidgets

from construct_ui.styled_property import StyledProperty


class Label(QtWidgets.QLabel):

    valid = StyledProperty('valid', True)

    def __init__(self, *args, **kwargs):
        super(Label, self).__init__(*args, **kwargs)
        StyledProperty.init(self)


class RightLabel(Label):

    def __init__(self, *args, **kwargs):
        super(RightLabel, self).__init__(*args, **kwargs)
        self.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)


class CenterLabel(Label):

    def __init__(self, *args, **kwargs):
        super(CenterLabel, self).__init__(*args, **kwargs)
        self.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
