# -*- coding: utf-8 -*-
from __future__ import absolute_import
from Qt import QtWidgets, QtCore, QtGui
from construct_ui import controls, forms, resources


def on_accepted(form):
    print(form.get_data())


def show_file_open_form():

    import sys
    from live import LiveStyle
    style = resources.style('dark')
    style_path = resources.style_path('dark')

    app = QtWidgets.QApplication(sys.argv)
    form = forms.FileOpenForm(construct.get_context())
    form.setStyleSheet(style)
    LiveStyle(style_path, form)
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

    WORK = 'Z:/Active_Projects/18-032-GOOGLE_2018_PRINT/production/sequences/gale/gale_hero_secondary/light/work/maya'
    import construct
    construct.init()
    construct.set_context_from_path(WORK)
    show_file_open_form()
