# -*- coding: utf-8 -*-
from __future__ import absolute_import
import sys

from Qt import QtWidgets, QtCore, QtGui

import construct
from construct_ui import controls, forms, resources


def apply_style(widget, style_name):
    from live import LiveStyle
    style = resources.style(style_name)
    style_path = resources.style_path(style_name)
    LiveStyle(style_path, widget)
    widget.setStyleSheet(style)


def show_file_open_form():

    # configure construct
    WORK = 'Z:/Active_Projects/18-032-GOOGLE_2018_PRINT/production/sequences/gale/gale_hero_secondary/light/work/maya'
    construct.init()
    construct.set_context_from_path(WORK)
    action = construct.actions.get('file.open')

    # show form
    app = QtWidgets.QApplication(sys.argv)
    apply_style(app, 'dark')

    form = forms.FileOpenForm(action)
    form.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    import bands

    class LoggingDispatcher(bands.Dispatcher):

        def __init__(self, name):
            self.name = name

        def dispatch(self, identifier, receiver, *args, **kwargs):
            print(self.name + '> Sending %s to %s' % (identifier, receiver))
            return receiver(*args, **kwargs)

    bands.get_band().dispatcher = LoggingDispatcher('bands')

    show_file_open_form()
