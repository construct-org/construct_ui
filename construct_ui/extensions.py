# -*- coding: utf-8 -*-
from __future__ import absolute_import
from construct import Extension
from construct_ui import FileOpenForm


class UIProvider(Extension):

    def load(self):
        self.add_form('file.open', FileOpenForm)
        self.add_form('file.save', FileSaveForm)
