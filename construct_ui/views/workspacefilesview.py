# -*- coding: utf-8 -*-
from __future__ import absolute_import
from Qt import QtWidgets, QtCore, QtCompat
from construct_ui.views.view import View


class WorkspaceFilesView(View, QtWidgets.QTreeView):

    def create(self):
        self.setSortingEnabled(True)
        QtCompat.setSectionResizeMode(
            self.header(),
            QtWidgets.QHeaderView.ResizeToContents
        )
        self.model = QtWidgets.QFileSystemModel(self)
        self.model.setFilter(QtCore.QDir.Files)
        self.setModel(self.model)

    def update(self):
        if self.data:
            extensions = self.data.config.get('extensions', [])
            name_filters = ['*' + ext for ext in extensions]
            self.model.setRootPath("")
            self.model.setRootPath(self.data.path)
            self.model.setNameFilters(name_filters)
            self.model.setNameFilterDisables(False)
            self.setRootIndex(self.model.index(self.data.path))

    def get_file(self):
        return self.model.filePath(self.currentIndex())
