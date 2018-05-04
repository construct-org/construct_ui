# -*- coding: utf-8 -*-
from __future__ import absolute_import

import construct
from construct_ui import resources
from Qt import QtWidgets


def ask(question, more=None):

    host = construct.get_host()
    parent = None
    if host:
        parent = host.get_qt_parent(QtWidgets.QMainWindow)

    dialog = QtWidgets.QMessageBox(parent)
    dialog.setStyleSheet(resources.style('dark'))
    dialog.setText(question)
    if more:
        dialog.setInformativeText(more)
    dialog.setStandardButtons(dialog.Yes | dialog.No)
    dialog.setSizePolicy(
        QtWidgets.QSizePolicy.Expanding,
        QtWidgets.QSizePolicy.Expanding,
    )

    response = dialog.exec_()
    if response == dialog.Yes:
        return True
    return False
