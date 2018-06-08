# -*- coding: utf-8 -*-
from __future__ import absolute_import
from abc import abstractmethod
from construct_ui.utils import ABCNonMeta, not_implemented


class View(ABCNonMeta):
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

    def __init__(self, data, *args, **kwargs):
        super(View, self).__init__(*args, **kwargs)
        self.initialized = False
        self.data = None
        self.set_data(data)
        self.create()
        self.update()
        self.initialized = True

    @not_implemented
    def will_set_data(self, old_data, data):
        return NotImplemented

    @not_implemented
    def set_data(self, data):
        if self.data is not data:
            self.will_set_data(self.data, data)
            self.data = data

        if not self.initialized:
            return

        self.update()

    @not_implemented
    def get_data(self):
        return self.data

    @abstractmethod
    def create(self):
        return NotImplemented

    @abstractmethod
    def update(self):
        return NotImplemented
