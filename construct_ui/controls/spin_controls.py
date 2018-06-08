# -*- coding: utf-8 -*-
from __future__ import absolute_import

from Qt import QtWidgets, QtCore

from construct_ui.controls.control import Control


class SpinControl(Control, QtWidgets.QWidget):
    '''Mixin for Controls using QSpinBox/QDoubleSpinBox as a control

    Attributes:
        name (str): Name of Control
        range (tuple): (minimum value, maximum value)
        default: Control default value
        parent (QWidget): Parent widget
    '''

    widget_cls = QtWidgets.QSpinBox
    default_range = (0, 99)

    def __init__(self, name, range=None, default=None, parent=None):
        self.range = range or self.default_range
        super(SpinControl, self).__init__(name, default, parent)

    def create(self):
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.widget = self.widget_cls(parent=self)
        self.layout.addWidget(self.widget)
        self.widget.valueChanged.connect(self.send_changed)

        self.set_range(self.range)

    def get_range(self):
        return self.widget.minimum(), self.widget.maximum()

    def set_range(self, range=None):
        range = range or self.default_range
        self.widget.setRange(*range)
        self.range = range

    def get(self):
        return self.widget.value()

    def set(self, value):
        self.widget.setValue(value)


class MultiSpinControl(Control, QtWidgets.QWidget):

    widget_cls = QtWidgets.QSpinBox
    default_range = (0, 99)
    num_controls = 2

    def __init__(self, name, ranges=None, default=None, parent=None):
        self.ranges = ranges or [
            self.default_range for i in range(self.num_controls)
        ]
        super(MultiSpinControl, self).__init__(name, parent)

    def create(self):
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.widgets = []
        for i in range(self.num_controls):
            box = self.widget_cls(parent=self.parent())
            box.valueChanged.connect(self.send_changed)
            self.layout.addWidget(box)
            self.widgets.append(box)

        self.set_ranges(self.ranges)

    def get_range(self, index):
        return self.ranges[index][0], self.ranges[index][1]

    def get_ranges(self):
        return self.ranges

    def set_range(self, index, range=None):
        range = range or self.default_range
        self.widgets[index].setRange(*range)
        self.ranges[index] = range

    def set_ranges(self, ranges):
        if len(ranges) != self.num_controls:
            raise ValueError('Expected %d ranges, got %d' %
                             (len(ranges), self.num_controls))
        for i, range in enumerate(ranges):
            self.set_range(i, range)

    def get(self):
        return tuple([box.value() for box in self.widgets])

    def set(self, value):
        if len(value) != self.num_controls:
            raise ValueError('Expected %d values, got %d' %
                             (len(value), self.num_controls))
        for box, value in zip(self.widgets, value):
            box.setValue(value)
