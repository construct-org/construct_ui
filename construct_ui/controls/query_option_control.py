# -*- coding: utf-8 -*-
from __future__ import absolute_import

from Qt import QtWidgets, QtCore

from construct_ui.controls.control import Control
from construct_ui.asynchronous import submit_async


class AnyCompleter(QtWidgets.QCompleter):

    def __init__(self, *args, **kwargs):
        super(AnyCompleter, self).__init__(*args, **kwargs)
        self.local_completion_prefix = ''
        self.set_delegate()

    def set_delegate(self):
        view = self.popup()
        view.setItemDelegate(QtWidgets.QStyledItemDelegate(view))
        view.setProperty('completer', True)

    def setModel(self, model):
        super(AnyCompleter, self).setModel(model)
        self.set_delegate()

    def updateModel(self):
        pattern = self.local_completion_prefix

        class ProxyModel(QtCore.QSortFilterProxyModel):
            def filterAcceptsRow(self, sourceRow, sourceParent):
                i = self.sourceModel().index(sourceRow, 0, sourceParent)
                data = self.sourceModel().data(i).lower()
                data_parts = data.split('/')
                pattern_parts = pattern.split('/')
                while pattern_parts:
                    part = pattern_parts.pop(0).lower()
                    for i, data_part in enumerate(data_parts):
                        if part in data_part:
                            data_parts = data_parts[i:]
                            break
                    else:
                        return False
                return True

        self.proxy_model = ProxyModel(self)
        self.proxy_model.setSourceModel(self.parent().model())
        super(AnyCompleter, self).setModel(self.proxy_model)

    def splitPath(self, path):
        self.local_completion_prefix = path
        self.updateModel()
        return ''


class QueryOptionControl(Control, QtWidgets.QComboBox):

    def __init__(self, name, query, formatter, default=None, parent=None):
        self.query = submit_async(query)
        self.formatter = formatter
        self.options = []
        self.models = []
        if default:
            self.models.append(default)
            self.options.append(self.formatter(default))
        super(QueryOptionControl, self).__init__(name, default, parent)

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
        self.setEditable(True)
        self.setInsertPolicy(self.NoInsert)
        self.activated.connect(self.send_changed)
        self.addItems(self.options)

        def after_completed(text):
            if text in self.options:
                index = self.options.index(text)
                self.setCurrentIndex(index)
                self.send_changed()

        self.completer = AnyCompleter(self)
        self.completer.setModel(self.model())
        self.completer.activated.connect(after_completed)
        self.setCompleter(self.completer)

        # Allow items to be styled
        self.styled_delegate = QtWidgets.QStyledItemDelegate(self.completer)
        self.setItemDelegate(self.styled_delegate)

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
