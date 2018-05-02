# -*- coding: utf-8 -*-
from __future__ import absolute_import
from Qt import QtWidgets, QtCore
from bands import channel
from construct import Context
from construct_ui.controls import EntryOptionControl
from construct_ui.views import View, WorkspaceFilesView


class FileOpenForm(View, QtWidgets.QWidget):

    accepted = channel('accepted')

    def will_set_data(self, old_data, data):
        self.ctx = data
        self.root = data.root
        self.workspace = data.workspace
        self.file = None

    def workspace_changed(self, control):
        ctx = Context.from_path(control.get().path)
        self.set_data(ctx)

    def accept(self):
        self.accepted.send(self)
        print(self.files.get_file())

    def create(self):

        # Make sure this fucker gets styled
        self.setAttribute(QtCore.Qt.WA_StyledBackground)

        # Setup workspace control
        if self.workspace:
            tags = self.workspace.tags
        else:
            tags = ['workspace']

        self.workspace_option = EntryOptionControl(
            'workspace',
            root=self.root,
            tags=tags,
            parent=self
        )
        self.workspace_option.set(self.workspace)
        self.workspace_option.changed.connect(self.workspace_changed)

        # Setup files view
        self.files = WorkspaceFilesView(
            self.workspace_option.get(),
            parent=self
        )
        self.files.doubleClicked.connect(self.accept)

        # Setup open button
        self.open_button = QtWidgets.QPushButton('Open', self)
        self.open_button.clicked.connect(self.accept)

        self.grid = QtWidgets.QGridLayout()
        self.grid.setContentsMargins(20, 20, 20, 20)
        self.grid.setColumnStretch(2, 1)
        self.grid.addWidget(QtWidgets.QLabel(self.workspace_option.name), 0, 0)
        self.grid.addWidget(self.workspace_option, 0, 1)
        self.grid.addWidget(self.files, 1, 0, 1, 4)
        self.grid.addWidget(self.open_button, 2, 3)

        self.setLayout(self.grid)

    def update(self):
        if self.workspace_option.get() is not self.workspace:
            self.workspace_option.set(self.workspace)
        self.files.set_data(self.workspace)
