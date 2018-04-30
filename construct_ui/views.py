# -*- coding: utf-8 -*-
from __future__ import absolute_import
from Qt import QtWidgets, QtCore
from abc import abstractmethod
from construct_ui.utils import ABCNonMeta, is_implemented, not_implemented


class View(ABCNonMeta):

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


class WorkspaceFilesView(View, QtWidgets.QTreeView):

    def create(self):
        self.setSortingEnabled(True)
        self.header().setResizeMode(self.header().ResizeToContents)
        self.model = QtWidgets.QFileSystemModel(self)
        self.model.setFilter(QtCore.QDir.Files)
        self.setModel(self.model)

    def update(self):
        if self.data:
            self.model.setRootPath("")
            self.model.setRootPath(self.data.path)
            self.setRootIndex(self.model.index(self.data.path))
