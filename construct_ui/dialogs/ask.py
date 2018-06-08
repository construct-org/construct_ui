# -*- coding: utf-8 -*-
from __future__ import absolute_import

import construct
from construct_ui import resources
from Qt import QtWidgets


def ask(question, more=None, title=None):

    host = construct.get_host()
    parent = None
    if host:
        parent = host.get_qt_parent()

    dialog = QtWidgets.QMessageBox(parent)
    dialog.setStyleSheet(resources.read(':/styles/dark'))
    dialog.setText(question)
    if more:
        dialog.setInformativeText(more)
    dialog.setStandardButtons(dialog.Yes | dialog.No)
    dialog.setSizePolicy(
        QtWidgets.QSizePolicy.Expanding,
        QtWidgets.QSizePolicy.Expanding,
    )
    if title:
        dialog.setWindowTitle(title)

    response = dialog.exec_()
    if response == dialog.Yes:
        return True
    return False
