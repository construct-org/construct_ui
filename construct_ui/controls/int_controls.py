# -*- coding: utf-8 -*-
from __future__ import absolute_import

from Qt import QtWidgets

from construct_ui.controls.spin_controls import SpinControl, MultiSpinControl
from construct_ui.controls.option_control import OptionControl


class IntControl(SpinControl):
    '''Int Control

    See also:
        SpinControl
    '''

    widget_cls = QtWidgets.QSpinBox
    default_range = (0, 99)


class Int2Control(MultiSpinControl):
    '''Int2 Control

    See also:
        MultiSpinControl
    '''

    widget_cls = QtWidgets.QSpinBox
    num_controls = 2


class Int3Control(MultiSpinControl):
    '''Int3 Control

    See also:
        MultiSpinControl
    '''

    widget_cls = QtWidgets.QSpinBox
    num_controls = 3


class IntOptionControl(OptionControl):

    def get(self):
        return self.currentIndex()

    def set(self, value):
        self.setCurrentIndex(value)
