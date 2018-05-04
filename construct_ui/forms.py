# -*- coding: utf-8 -*-
from __future__ import absolute_import
from Qt import QtWidgets, QtCore
from bands import channel
from abc import abstractmethod
import construct
from construct_ui.controls import QueryOptionControl
from construct_ui.views import View, WorkspaceFilesView


class ActionForm(View):
    '''An interface to run an Action.

    The data of an ActionForm is either the current construct Context or a
    Context object passed to ActionForm. Subclasses must implement get_kwargs
    returning the keyword arguments to pass their Actions. Subclasses may
    override get_context to customize the context in which their Action will run. Subclasses may override on_accept to customize how their Action is run once the form is accepted.
    '''


    def __init__(self, action, ctx=None, *args, **kwargs):
        self.action = action
        ctx = ctx or construct.get_context()
        super(ActionForm, self).__init__(ctx, *args, **kwargs)

        self.accepted.connect(self.on_accept)
        self.rejected.connect(self.on_reject)
        if hasattr(self, 'setWindowTitle'):
            self.setWindowTitle(action.label)

    def on_accept(self):
        action_args = self.get_args()
        action_kwargs = self.get_kwargs()
        action_ctx = self.get_context()
        action_kwargs['ctx'] = action_ctx
        action = self.action(*action_args, **action_kwargs)
        self.close()
        action.run()

    def on_reject(self):
        self.close()

    def get_args(self):
        '''Return args to pass to the form's Action'''

        return ()

    @abstractmethod
    def get_kwargs(self):
        '''Return kwargs to pass to the form's Action'''

        return NotImplemented

    def get_context(self):
        '''Return context in which to run to the form's Action'''

        return self.data


class FileOpenForm(ActionForm, QtWidgets.QDialog):

    def get_kwargs(self):
        return dict(file=self.files.get_file())

    def workspace_changed(self, control):
        ctx = construct.Context.from_path(control.get().path)
        self.set_data(ctx)

    def create(self):
        # Make sure this fucker gets styled
        self.setAttribute(QtCore.Qt.WA_StyledBackground)

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

        query = construct.search(root=self.data.root, tags=tags)

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
        self.grid.setColumnStretch(0, 1)
        self.grid.addWidget(self.workspace_option, 0, 0, 1, 3)
        self.grid.addWidget(self.files, 1, 0, 1, 3)
        self.grid.addWidget(self.cancel_button, 2, 1)
        self.grid.addWidget(self.open_button, 2, 2)

        self.setLayout(self.grid)

    def update(self):
        if self.workspace_option.get() is not self.data.workspace:
            self.workspace_option.set(self.data.workspace)
        self.files.set_data(self.data.workspace)
