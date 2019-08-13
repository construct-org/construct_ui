# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
from Qt import QtWidgets, QtCore, QtGui
import construct
from construct import utils
from construct_ui.controls import (
    QueryOptionControl,
    IntControl,
    StringControl,
    OptionControl
)
from construct_ui.forms.actionform import ActionForm
from construct_ui.widgets import RightLabel, Label


class SetWorkspaceForm(ActionForm, QtWidgets.QDialog):

    def get_kwargs(self):
        return dict(task=self.task_option.get())

    def create(self):

        params = self.action.parameters(self.data)

        # Make sure the form gets styled
        self.setAttribute(QtCore.Qt.WA_StyledBackground)

        # Setup project control
        def format_project(project):
            return project.name

        query = construct.search(
            root=self.data.root,
            tags=['project'],
            depth=1,
            levels=1
        )

        self.project_option = QueryOptionControl(
            'project',
            query=query,
            formatter=format_project,
            default=self.data.project,
            parent=self
        )
        self.project_option.changed.connect(self.project_changed)

        # Setup task control
        def format_task(task):
            parents = list(task.parents())[::-1]
            if parents:
                parts = parents[1:] + [task]
                return '/'.join([p.name for p in parts])
            else:
                return task.name

        tags = ['task']

        query = construct.search(root=self.data.project.path, tags=tags)

        self.task_option = QueryOptionControl(
            'task',
            query=query,
            formatter=format_task,
            default=self.data.task,
            parent=self
        )
        self.task_option.changed.connect(self.task_changed)

        # Setup save button
        self.set_workspace_button = QtWidgets.QPushButton('Set', self)
        self.set_workspace_button.clicked.connect(self.accept)

        self.grid = QtWidgets.QGridLayout()
        self.grid.setContentsMargins(20, 20, 20, 20)
        self.grid.setVerticalSpacing(20)
        self.grid.setColumnStretch(1, 1)
        self.grid.setRowStretch(2, 1)

        # Location controls
        self.grid.addWidget(RightLabel('Project'), 0, 0)
        self.grid.addWidget(self.project_option, 0, 1, 1, 3)
        self.grid.addWidget(RightLabel('Task'), 1, 0)
        self.grid.addWidget(self.task_option, 1, 1, 1, 3)

        # Buttons
        self.grid.addWidget(self.set_workspace_button, 3, 3)

        self.setLayout(self.grid)

    def cleanup(self):
        self.project_option.stop_query()
        self.task_option.stop_query()

    def update(self):
        if self.project_option.get() is not self.data.project:
            self.project_option.set(self.data.project)
        if self.task_option.get() is not self.data.task:
            self.task_option.set(self.data.task)

    def project_changed(self, control):
        tags = self.data.task.tags
        project = control.get()
        task = project.children().tags(*tags).one()
        query = project.children().tags(*tags)
        self.task_option.set_query(query, task)

    def task_changed(self, control):
        ctx = construct.Context.from_path(control.get().path)
        self.set_data(ctx)
