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
        form.setStyleSheet(resources.style('dark'))
        return form

    return None


def main():
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
    apply_style(app, 'dark')

    # Show some forms
    form = form_for_action('file.open')
    apply_style(form, 'dark')
    form.exec_()

    form = form_for_action('file.save')
    apply_style(form, 'dark')
    form.show()

    # Wait for app loop to finish and exit
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
