# -*- coding: utf-8 -*-
from __future__ import absolute_import
from Qt import QtWidgets, QtCore, QtGui
from construct_ui import controls, forms

def map_controls():

    data = {
        'bool': True,
        'int': 10,
        'int2': [10, 20],
        'int3': [10, 20, 30],
        'float': 10,
        'float2': [10, 20],
        'float3': [10, 20, 30],
        'string': 'hello world!',
        'option': ['one', 'two', 'three', 'four']
    }

    import sys
    app = QtWidgets.QApplication(sys.argv)
    win = QtWidgets.QWidget()
    layout = QtWidgets.QFormLayout()
    controls = []

    for name, value in data.items():
        control = control_for_value(value)
        c = control(name, parent=win)
        controls.append(c)
        if isinstance(c, controls.OptionControl):
            c.set_options(value)
        else:
            c.set(value)
        layout.addRow(c.name, c)

    win.setLayout(layout)
    win.show()
    def closeEvent(event):
        print({c.name: c.get() for c in controls})
        event.accept()
    win.closeEvent = closeEvent
    sys.exit(app.exec_())


def show_controls():

    import sys
    app = QtWidgets.QApplication(sys.argv)
    win = QtWidgets.QWidget()
    layout = QtWidgets.QFormLayout()

    for control in CONTROL_TYPES:
        c = control(control.__name__, parent=win)
        layout.addRow(c.name, c)

    win.setLayout(layout)
    win.show()
    sys.exit(app.exec_())


def show_file_open_form():

    import sys
    app = QtWidgets.QApplication(sys.argv)
    form = forms.FileOpenForm(construct.get_context())
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

    import construct
    construct.init()
    show_file_open_form()
