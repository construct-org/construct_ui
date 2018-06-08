# -*- coding: utf-8 -*-
from __future__ import absolute_import

from Qt import QtWidgets

from construct_ui.controls.spin_controls import SpinControl, MultiSpinControl


class FloatControl(SpinControl):
    '''Float Control

    See also:
        SpinControl
    '''

    widget_cls = QtWidgets.QDoubleSpinBox
    default_range = (0, 99)


class Float2Control(MultiSpinControl):
    '''Float2 Control

    See also:
        MultiSpinControl
    '''

    widget_cls = QtWidgets.QDoubleSpinBox
    num_controls = 2


class Float3Control(MultiSpinControl):
    '''Float3 Control

    See also:
        MultiSpinControl
    '''

    widget_cls = QtWidgets.QDoubleSpinBox
    num_controls = 3
