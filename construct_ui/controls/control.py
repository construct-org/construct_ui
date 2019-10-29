# -*- coding: utf-8 -*-
from __future__ import absolute_import

from abc import abstractmethod

from bands import channel

from construct_ui.utils import ABCNonMeta
from construct_ui.styled_property import StyledProperty


# This was a subclass of ABCNonMeta
# Nuke12 is using an outdated version of PySide2 that has issues with __new__
class Control(object):
    '''
    Mixin base class for all Control widgets. The purpose of the Control Mixin
    is to ensure a unified API across all Control widgets.

      - Controls emit a **changed** messaged when their control's value changes
      - `Control.get` returns the value of a Control
      - `Control.set` sets the value of a Control

    Control should be used as the first base class of a control QWidget.

    Subclasses must use the create method to setup and create their widget/s.
    Users should call the send_changed method when their contol widget's value
    changes. Subclasses must also implement the get and set methods.

    Arguments:
        name (str): Name of the control
        range (tuple): (min, max)
        default (int): Default value
        parent (QWidget): Parent widget

    Attributes:
        changed (bands.channel): Emitted when a Control's value is changed.
        name (str): Control name
        default: Control's default value
        valid (StyledProperty): True when control value is valid
        error (StyledProperty): True when control value is invalid

    Example:
        Here is how we would implement a simple IntControl::

            class IntControl(Control, QtWidgets.QSpinBox):

                def create(self):
                    self.setRange(0, 99)
                    self.valueChanged.connect(self.send_changed)

                def get(self):
                    return self.value()

                def set(self, value):
                    return self.setValue(value)

            int_cntrl = IntControl()
            int_cntrl.set(10)
            assert int_cntrl.get() == 10
    '''

    changed = channel('changed')
    valid = StyledProperty('valid', True)
    error = StyledProperty('error', False)

    def __init__(self, name, default=None, parent=None):
        super(Control, self).__init__(parent=parent)

        self.setObjectName(name)
        self.name = name
        self.create()
        if default is not None:
            self.set(default)

        StyledProperty.init(self)

    def send_changed(self):
        self.changed.send(self)

    @abstractmethod
    def create(self):
        return NotImplemented

    @abstractmethod
    def get(self):
        return NotImplemented

    @abstractmethod
    def set(self, value):
        return NotImplemented
