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


class FileSaveForm(ActionForm, QtWidgets.QDialog):

    def get_kwargs(self):
        return dict(
            workspace=self.workspace_option.get(),
            name=self.name_control.get(),
            version=self.version_control.get(),
            ext=self.ext_control.get(),
        )

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

        # Setup workspace control
        def format_workspace(workspace):
            parents = list(workspace.parents())[::-1]
            if parents:
                parts = parents[1:] + [workspace]
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

        # Setup filenaming options

        self.name_control = StringControl(
            'name',
            default=params['name']['default'],
            parent=self
        )
        self.name_validator = QtGui.QRegExpValidator(
            QtCore.QRegExp('[A-Za-z0-9_]+')
        )
        self.name_control.setValidator(self.name_validator)
        self.name_control.changed.connect(self.update_version)
        self.version_control = IntControl(
            'name',
            range=[1, 999],
            default=params['version']['default'],
            parent=self
        )
        self.version_control.changed.connect(self.update_preview)
        self.ext_control = OptionControl(
            'ext',
            options=params['ext']['options'],
        )
        self.ext_control.changed.connect(self.update_version)

        self.name_preview = Label(self.generate_preview())

        # Setup save button
        self.save_button = QtWidgets.QPushButton('Save', self)
        self.save_button.clicked.connect(self.accept)

        self.grid = QtWidgets.QGridLayout()
        self.grid.setContentsMargins(20, 20, 20, 20)
        self.grid.setVerticalSpacing(20)
        self.grid.setRowMinimumHeight(2, 36)
        self.grid.setColumnStretch(1, 1)
        self.grid.setRowStretch(3, 1)

        # Location controls
        self.grid.addWidget(RightLabel('Project'), 0, 0)
        self.grid.addWidget(self.project_option, 0, 1, 1, 3)
        self.grid.addWidget(RightLabel('Workspace'), 1, 0)
        self.grid.addWidget(self.workspace_option, 1, 1, 1, 3)

        # File name controls
        ngrid = QtWidgets.QGridLayout()
        ngrid.setContentsMargins(0, 0, 0, 0)
        ngrid.setHorizontalSpacing(8)
        ngrid.setColumnStretch(0, 1)
        ngrid.addWidget(self.name_control, 0, 0)
        ngrid.addWidget(self.version_control, 0, 1)
        ngrid.addWidget(self.ext_control, 0, 2)
        self.grid.addWidget(RightLabel('Name'), 2, 0)
        self.grid.addLayout(ngrid, 2, 1, 1, 3)

        # Preview
        # self.grid.addWidget(RightLabel('Preview'), 3, 0)
        self.grid.addWidget(self.name_preview, 4, 1, 1, 2)

        # Buttons
        # self.grid.addWidget(self.cancel_button, 5, 2)
        self.grid.addWidget(self.save_button, 4, 3)

        self.setLayout(self.grid)

    def cleanup(self):
        self.project_option.stop_query()
        self.workspace_option.stop_query()

    def update(self):
        if self.project_option.get() is not self.data.project:
            self.project_option.set(self.data.project)
        if self.workspace_option.get() is not self.data.workspace:
            self.workspace_option.set(self.data.workspace)

        params = self.action.parameters(self.data)
        self.name_control.set(params['name']['default'])
        self.version_control.set(params['version']['default'])
        self.ext_control.set(params['ext']['default'])
        self.update_preview()

    def project_changed(self, control):
        tags = self.data.workspace.tags
        project = control.get()
        workspace = project.children().tags(*tags).one()
        query = project.children().tags(*tags)
        self.workspace_option.set_query(query, workspace)

    def workspace_changed(self, control):
        ctx = construct.Context.from_path(control.get().path)
        self.set_data(ctx)

    def update_version(self, control):
        workspace = self.data.workspace
        name = self.name_control.get()
        ext = self.ext_control.get()
        next_version = workspace.get_next_version(name, ext)
        self.version_control.set(next_version)
        self.update_preview()

    def update_preview(self, *args):
        new_filename = self.generate_preview()
        self.name_preview.setText(new_filename)
        full_path = utils.unipath(self.data.workspace.path, new_filename)
        self.name_preview.valid = not os.path.exists(full_path)

    def generate_preview(self):
        data = self.get_kwargs()
        data['task'] = self.data
        data['version'] = '{0:>3d}'.format(data['version'])
        tmpl = construct.get_path_template('workspace_file')
        return tmpl.format(dict(
            task=self.data.task.short,
            name=self.name_control.get(),
            version='{:0>3d}'.format(self.version_control.get()),
            ext=self.ext_control.get()
        ))
