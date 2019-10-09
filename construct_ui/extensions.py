# -*- coding: utf-8 -*-
from __future__ import absolute_import
from construct import Extension


class ActionUIProvider(Extension):

    name = 'Action UI Provider'
    attr_name = 'action_ui_provider'

    def available(self, ctx):
        try:
            import Qt
            return True
        except ImportError:
            return False

    def load(self):
        from construct_ui import forms
        self.add_form('file.open', forms.FileOpenForm)
        self.add_form('file.save', forms.FileSaveForm)
        self.add_form('set_workspace', forms.SetWorkspaceForm)
        self.add_form('publish', forms.PublishForm)
