# -*- coding: utf-8 -*-
from __future__ import absolute_import
from Qt import QtWidgets, QtCore
import construct
from construct_ui.controls import QueryOptionControl
from construct_ui.forms.actionform import ActionForm
from construct_ui.views import WorkspaceFilesView
from construct_ui.widgets import RightLabel


class FileOpenForm(ActionForm, QtWidgets.QDialog):

    def get_kwargs(self):
        return dict(file=self.files.get_file())

    def create(self):
        # Make sure the form gets styled
        self.setAttribute(QtCore.Qt.WA_StyledBackground)

        # Setup project control
        def format_project(project):
            return project.name

        query = construct.search(
            root=self.data.root,
            tags=['project'],
            depth=2
        )

        self.project_option = QueryOptionControl(
            'project',
            query=query,
            formatter=format_project,
            default=self.data.project,
            parent=self
        )
        self.project_option.changed.connect(self.project_changed)

        # Setup workspace control
        def format_workspace(workspace):
            parents = list(workspace.parents())[::-1]
            if parents:
                parts = parents[max(0, len(parents) - 3):] + [workspace]
                return '/'.join([p.name for p in parts])
            else:
                return workspace.name

        if self.data.workspace:
            tags = self.data.workspace.tags
        else:
            tags = ['workspace']

        query = construct.search(root=self.data.project.path, tags=tags)

        self.workspace_option = QueryOptionControl(
            'workspace',
            query=query,
            formatter=format_workspace,
            default=self.data.workspace,
            parent=self
        )
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
        self.cancel_button = QtWidgets.QPushButton('Cancel', self)
        self.cancel_button.clicked.connect(self.reject)

        self.grid = QtWidgets.QGridLayout()
        self.grid.setContentsMargins(20, 20, 20, 20)
        self.grid.setVerticalSpacing(20)
        self.grid.setColumnStretch(1, 1)
        self.grid.addWidget(RightLabel('Project'), 0, 0)
        self.grid.addWidget(self.project_option, 0, 1, 1, 3)
        self.grid.addWidget(RightLabel('Workspace'), 1, 0)
        self.grid.addWidget(self.workspace_option, 1, 1, 1, 3)
        self.grid.addWidget(self.files, 2, 0, 1, 4)
        self.grid.addWidget(self.cancel_button, 3, 2)
        self.grid.addWidget(self.open_button, 3, 3)

        self.setLayout(self.grid)

    def cleanup(self):
        self.project_option.stop_query()
        self.workspace_option.stop_query()

    def update(self):
        if self.project_option.get() is not self.data.project:
            self.project_option.set(self.data.project)
        if self.workspace_option.get() is not self.data.workspace:
            self.workspace_option.set(self.data.workspace)
        self.files.set_data(self.data.workspace)

    def sizeHint(self):
        return QtCore.QSize(560, 480)

    def project_changed(self, control):
        tags = self.data.workspace.tags
        project = control.get()
        workspace = project.children(*tags).one()

        query = project.children(*tags)
        self.workspace_option.set_query(query, workspace)

    def workspace_changed(self, control):
        ctx = construct.Context.from_path(control.get().path)
        self.set_data(ctx)
