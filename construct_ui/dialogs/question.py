# -*- coding: utf-8 -*-
from __future__ import absolute_import

import construct
from construct_ui.dialogs.frameless_dialog import FramelessDialog
from construct_ui.widgets import Label
from construct_ui import resources
from Qt import QtWidgets


class Question(FramelessDialog):

    def __init__(self, question, more=None, title=None, parent=None):
        super(Question, self).__init__(title or '', parent)

        self.question_label = Label(question, self)
        self.more_label = Label(parent=self)
        if more:
            self.more_label.setText(more)

        self.buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Yes |
            QtWidgets.QDialogButtonBox.No
        )
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        self.layout.addWidget(self.question_label)
        self.layout.addWidget(self.more_label)
        self.layout.addStretch(1)
        self.layout.addWidget(self.buttons)


def ask(question, more=None, title=None):
    '''Popup a dialog asking a question.

    Arguments:
        question (str): The question to ask.
        more (str): Optional second line of text.
        title (str): Optional window title.

    Returns:
        True if dialog is accepted.
    '''

    try:
        host = construct.get_host()
        parent = host.get_qt_parent()
    except AttributeError:
        parent = None

    dialog = Question(question, more, title, parent)
    dialog.setStyleSheet(resources.style(':/styles/dark'))

    return bool(dialog.exec_())
