# -*- coding: utf-8 -*-
from __future__ import absolute_import

import construct
from construct_ui.dialogs.frameless_dialog import FramelessDialog
from construct_ui.widgets import Label
from construct_ui import resources
from Qt import QtWidgets


class Notice(FramelessDialog):

    def __init__(self, header, body, title, parent=None):
        super(Notice, self).__init__(title or '', parent)

        self.header_label = Label(header, self)
        self.body_label = QtWidgets.QTextEdit(parent=self)
        self.body_label.setPlainText(body)
        self.buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok
        )
        self.buttons.accepted.connect(self.accept)

        self.layout.addWidget(self.header_label)
        self.layout.addWidget(self.body_label)
        self.layout.addStretch(1)
        self.layout.addWidget(self.buttons)
        self.setMaximumWidth(1024)
        self.adjustSize()


def error(header, body, title='Error'):
    '''Popup a dialog asking a question.

    Arguments:
        header (str): The header text
        body (str): The body text
        title (str): Custom window title

    Returns:
        True when dialog is accepted
    '''

    try:
        host = construct.get_host()
        parent = host.get_qt_parent()
    except AttributeError:
        parent = None

    dialog = Notice(header, body, title, parent)
    dialog.setStyleSheet(resources.style(construct.config['STYLE']))

    return bool(dialog.exec_())
