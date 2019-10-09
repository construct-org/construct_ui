# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
from Qt import QtWidgets, QtCore, QtGui
import construct
from construct_ui.forms.actionform import ActionForm
from construct_ui.dialogs import FramelessDialog
from construct_ui.widgets import Label, Icon
from construct_ui.utils import pix


# TEMPORARY PUBLISH FORM - JUST A SIMPLE TEXT DIALOG


class PublishForm(ActionForm, QtWidgets.QDialog):
    '''This is a temporary Publish form'''

    def get_kwargs(self):
        return {}

    def create(self):

        self._mouse_pressed = False
        self._mouse_position = None
        self.setWindowFlags(
            QtCore.Qt.Dialog |
            QtCore.Qt.FramelessWindowHint
        )
        self.setMouseTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding,
        )

        self.title_label = QtWidgets.QLabel()
        self.title_label.setProperty('titlebar', True)
        self.title_label.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum,
        )
        self.title_label.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.title_label.setFocusPolicy(QtCore.Qt.NoFocus)
        self.close_button = Icon(':/icons/close', size=24)
        self.close_button.clicked.connect(self.reject)
        self.titlebar_layout = QtWidgets.QHBoxLayout()
        self.titlebar_layout.addWidget(self.title_label)
        self.titlebar_layout.addStretch(1)
        self.titlebar_layout.addWidget(self.close_button)
        self.titlebar_layout.setContentsMargins(0, 0, 0, 0)

        self.title_label.setFocus()

        self.title_label.setText('Publish ' + os.path.basename(self.data.file))
        self.question_label = Label(
            'Would you like to publish the current workfile?',
            parent=self,
        )
        self.more_label = Label(
            (
                '- Save current workfile\n'
                '- Flatten references\n'
                '- Save publish file\n'
                '- Open next workfile'
            ),
            parent=self,
        )

        self.buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Yes |
            QtWidgets.QDialogButtonBox.No
        )
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        self.layout = QtWidgets.QVBoxLayout()
        margin = [pix(16)] * 4
        spacing = pix(20)
        self.layout.setSpacing(spacing)
        self.layout.setContentsMargins(*margin)
        self.layout.addWidget(self.question_label)
        self.layout.addWidget(self.more_label)
        self.layout.addStretch(1)
        self.layout.addWidget(self.buttons)

        self.grid_layout = QtWidgets.QGridLayout()
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.addLayout(self.titlebar_layout, 0, 0)
        self.grid_layout.setRowStretch(1, 1)
        self.grid_layout.addLayout(self.layout, 1, 0)
        self.setLayout(self.grid_layout)

    def cleanup(self):
        pass

    def update(self):
        pass

    def mousePressEvent(self, event):
        if event.buttons() & QtCore.Qt.LeftButton:
            pos = event.pos()
            self._mouse_pressed = True
            self._mouse_position = pos

    def mouseMoveEvent(self, event):
        if self._mouse_pressed:
            vector = event.pos() - self._mouse_position
            self.move(self.mapToParent(vector))

    def mouseReleaseEvent(self, event):
        self._mouse_pressed = False
        self._mouse_position = None

    def minimumSizeHint(self):
        return QtCore.QSize(640, 480)
