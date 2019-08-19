# -*- coding: utf-8 -*-
from __future__ import absolute_import
import sys

from Qt import QtWidgets, QtCore

import construct
from construct_ui import resources, dialogs, widgets


def apply_style(widget, style_name):
    from live import LiveStyle
    style = resources.read(style_name)
    style_path = resources.path(style_name)
    LiveStyle(style_path, widget)
    widget.setStyleSheet(style)


def ask_a_question():
    app = QtWidgets.QApplication(sys.argv)
    resources.init()

    if dialogs.ask('Are you okay?', 'seriously', 'AYO'):
        print('YAY!')
    sys.exit()


def show_frameless_dialog():
    app = QtWidgets.QApplication(sys.argv)
    resources.init()

    dialog = dialogs.FramelessDialog('Hello World')
    apply_style(dialog, ':/styles/dark')

    sys.exit(dialog.exec_())


def show_collapsable_list():
    app = QtWidgets.QApplication(sys.argv)
    resources.init()

    ls = widgets.CollapsableList('Projects')
    ls.list_widget.addItems(['Project ' + char for char in 'ABCDEFGH'])
    apply_style(ls, ':/styles/dark')
    ls.show()

    sys.exit(app.exec_())


def show_header():

    def null():
        print('Action')

    app = QtWidgets.QApplication(sys.argv)
    resources.init()

    dialog = QtWidgets.QDialog()
    apply_style(dialog, ':/styles/dark')

    header = widgets.Header('Hello World!')
    header.add_menu_item('Item 1', null)
    header.add_menu_item('Item 2', null)
    header.add_menu_item('Item 3', null)
    header.add_menu_item('Item 4', null)
    layout = QtWidgets.QVBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)
    layout.addWidget(header)
    layout.setAlignment(QtCore.Qt.AlignTop)
    dialog.setLayout(layout)

    sys.exit(dialog.exec_())


def form_for_action(action_or_identifier):

    if construct.action.is_action_type(action_or_identifier):
        action = action_or_identifier
    else:
        action = construct.actions.get(action_or_identifier)

    try:
        host = construct.get_host()
        parent = host.get_qt_parent()
    except AttributeError:
        host = None
        parent = None

    form_cls = construct.get_form(action.identifier)
    if form_cls:
        form = form_cls(action, construct.get_context(), parent)
        form.setStyleSheet(resources.style(':/styles/dark'))
        return form

    return None


def show_action_forms():
    # configure bands
    import bands

    class LoggingDispatcher(bands.Dispatcher):

        def __init__(self, name):
            self.name = name

        def dispatch(self, identifier, receiver, *args, **kwargs):
            print(self.name + '> Sending %s to %s' % (identifier, receiver))
            return receiver(*args, **kwargs)

    bands.get_band().dispatcher = LoggingDispatcher('bands')

    # configure construct
    construct.init()
    workspace = construct.search(tags=['workspace']).one()
    construct.set_context_from_entry(workspace)

    # configure qapp with dynamic stylesheet
    app = QtWidgets.QApplication(sys.argv)
    resources.init()
    apply_style(app, ':/styles/dark')

    # Show some forms
    form = form_for_action('file.open')
    apply_style(form, ':/styles/dark')
    form.exec_()

    form = form_for_action('file.save')
    apply_style(form, ':/styles/dark')
    form.show()

    # Wait for app loop to finish and exit
    sys.exit(app.exec_())


if __name__ == '__main__':
    show_header()
