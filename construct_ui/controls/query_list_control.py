# -*- coding: utf-8 -*-
from __future__ import absolute_import

from Qt import QtWidgets, QtCore

from construct_ui.controls.control import Control
from construct_ui.asynchronous import submit_async
from construct_ui.widgets.lists import CollapsableList


class QueryListControl(Control, CollapsableList):

    def __init__(self, name, query, formatter, default=None, parent=None):
        self.query = submit_async(query)
        self.formatter = formatter
        self.options = []
        self.models = []
        if default:
            self.models.append(default)
            self.options.append(self.formatter(default))
        super(QueryListControl, self).__init__(name, default, parent)

    def stop_query(self):
        self.query.stop_later()

    def set_query(self, query, default=None):
        self.stop_query()
        self.clear()
        self.options = []
        self.models = []
        if default:
            self.models.append(default)
            self.options.append(self.formatter(default))
            self.addItem(self.options[0])
            self.set(default)
            self.send_changed()

        self.query = submit_async(query)
        self.query.on_result(self.add_model)
        self.query.start()

    def add_model(self, model):
        if model not in self.models:
            self.models.append(model)
            item = self.formatter(model)
            self.options.append(item)
            self.addItem(item)

    def create(self):
        # Set it up

        # Run query thread
        self.query.on_result(self.add_model)
        self.query.start()

    def get(self):
        index = self.currentIndex()
        return self.models[index]

    def set(self, value):
        try:
            index = self.models.index(value)
            self.setCurrentIndex(index)
        except ValueError:
            pass
