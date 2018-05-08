# -*- coding: utf-8 -*-
from __future__ import absolute_import
from Qt import QtWidgets


class Label(QtWidgets.QLabel):

    def __init__(self, text, align='left', parent=None):
        super(Label, self).__init__(text, parent)
        self.setProperty('align', align)


class RightLabel(Label):

    def __init__(self, text, parent=None):
        super(RightLabel, self).__init__(text, 'right', parent)


class CenterLabel(Label):

    def __init__(self, text, parent=None):
        super(CenterLabel, self).__init__(text, 'center', parent)
