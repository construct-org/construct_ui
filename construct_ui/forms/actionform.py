# -*- coding: utf-8 -*-
from __future__ import absolute_import
from abc import abstractmethod
from Qt import QtCore
import construct
from construct_ui.views import View


class ActionForm(View):
    '''An interface to run an Action.

    The data of an ActionForm is either the current construct Context or a
    Context object passed to ActionForm. Subclasses must implement get_kwargs
    returning the keyword arguments to pass their Actions. Subclasses may
    override get_context to customize the context in which their Action will
    run. Subclasses may override on_accept to customize how their Action is
    run once the form is accepted.
    '''

    def __init__(self, action, ctx=None, *args, **kwargs):
        self.action = action
        ctx = ctx or construct.get_context()
        super(ActionForm, self).__init__(ctx, *args, **kwargs)

        self.accepted.connect(self.on_accept)
        self.rejected.connect(self.on_reject)
        if hasattr(self, 'setWindowTitle'):
            self.setWindowTitle(action.label)
            self.setWindowFlags(
                self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint
            )

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
