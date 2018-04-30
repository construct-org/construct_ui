# -*- coding: utf-8 -*-
from __future__ import absolute_import
from Qt import QtWidgets
from bands import channel
from construct import Context
from construct_ui.controls import EntryOptionControl
from construct_ui.views import View, WorkspaceFilesView


class FileOpenForm(View, QtWidgets.QWidget):

    def will_set_data(self, old_data, data):
        self.root = data.root
        self.workspace = data.workspace

    def workspace_changed(self, control):
        ctx = Context.from_path(control.get().path)
        self.set_data(ctx)

    def create(self):
        self.workspace_option = EntryOptionControl(
            'workspace',
            root=self.root,
            tags=['workspace', 'maya'],
            parent=self
        )
        self.workspace_option.set(self.workspace)
        self.files = WorkspaceFilesView(
            self.workspace_option.get(),
            parent=self
        )

        self.workspace_option.changed.connect(self.workspace_changed)

        self.grid = QtWidgets.QGridLayout()
        self.grid.setColumnStretch(2, 1)
        self.grid.addWidget(QtWidgets.QLabel(self.workspace_option.name), 0, 0)
        self.grid.addWidget(self.workspace_option, 0, 1)
        self.grid.addWidget(self.files, 1, 0, 1, 3)

        self.setLayout(self.grid)

    def update(self):
        if self.workspace_option.get() is not self.workspace:
            self.workspace_option.set(self.workspace)
        self.files.set_data(self.workspace)
