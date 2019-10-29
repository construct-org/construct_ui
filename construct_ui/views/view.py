# -*- coding: utf-8 -*-
from __future__ import absolute_import
from abc import abstractmethod
from construct_ui.utils import ABCNonMeta, not_implemented


# This was a subclass of ABCNonMeta
# Nuke12 is using an outdated version of PySide2 that has issues with __new__
class View(object):
    '''
    Mixin base class for all View widgets. The purpose of the View Mixin
    is to ensure a unified API across all View widgets.

    View should be used as the first base class of a view QWidget.

    Subclasses must use the create method to setup and create their widget/s.
    Users should call the send_changed method when their contol widget's value
    changes. Subclasses must also implement the get and set methods.

    Arguments:
        name (str): Name of the control
        data (object): Object this view acts on
        parent (QWidget): Parent widget
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
