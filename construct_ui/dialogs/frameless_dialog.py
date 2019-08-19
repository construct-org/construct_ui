# -*- coding: utf-8 -*-
from __future__ import absolute_import

from Qt import QtWidgets, QtCore

from construct_ui.widgets import Icon
from construct_ui.utils import pix


class FramelessDialog(QtWidgets.QDialog):

    _resize_area_map = {
        (False, False, False, False): None,
        (True, False, False, False): 'left',
        (True, True, False, False): 'topLeft',
        (False, True, False, False): 'top',
        (False, True, True, False): 'topRight',
        (False, False, True, False): 'right',
        (False, False, True, True): 'bottomRight',
        (False, False, False, True): 'bottom',
        (True, False, False, True): 'bottomLeft'
    }
    _cursor_map = {
        None: QtCore.Qt.ArrowCursor,
        'left': QtCore.Qt.SizeHorCursor,
        'topLeft': QtCore.Qt.SizeFDiagCursor,
        'top': QtCore.Qt.SizeVerCursor,
        'topRight': QtCore.Qt.SizeBDiagCursor,
        'right': QtCore.Qt.SizeHorCursor,
        'bottomRight': QtCore.Qt.SizeFDiagCursor,
        'bottom': QtCore.Qt.SizeVerCursor,
        'bottomLeft': QtCore.Qt.SizeBDiagCursor
    }

    def __init__(self, title, parent=None):
        super(FramelessDialog, self).__init__(parent=parent)

        self._mouse_pressed = False
        self._mouse_position = None
        self._resize_area = None
        self.resize_area_size = 16

        self.setWindowFlags(
            QtCore.Qt.Dialog |
            QtCore.Qt.FramelessWindowHint
        )
        self.setMouseTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding,
        )

        self.title_label = QtWidgets.QLabel(title)
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

        self.grid_layout = QtWidgets.QGridLayout()
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.addLayout(self.titlebar_layout, 0, 0)
        self.grid_layout.setRowStretch(1, 1)
        self.layout = QtWidgets.QVBoxLayout()
        margin = [pix(16)] * 4
        spacing = pix(20)
        self.layout.setSpacing(spacing)
        self.layout.setContentsMargins(*margin)
        self.grid_layout.addLayout(self.layout, 1, 0)

        self.title_label.setFocus()
        self.setLayout(self.grid_layout)

    @property
    def resizing(self):
        return bool(self._resize_area)

    def _check_resize_area(self, pos):

        x, y = pos.x(), pos.y()
        self._resize_area = self._resize_area_map[(
            x < self.resize_area_size,
            y < self.resize_area_size,
            x > self.width() - self.resize_area_size,
            y > self.height() - self.resize_area_size,
        )]

    def mousePressEvent(self, event):

        if event.buttons() & QtCore.Qt.LeftButton:
            pos = event.pos()
            self._check_resize_area(pos)
            self._mouse_pressed = True
            self._mouse_position = pos

    def mouseMoveEvent(self, event):

        if not self._mouse_pressed:
            pos = event.pos()
            self._check_resize_area(pos)
            cursor = self._cursor_map.get(self._resize_area)
            self.setCursor(cursor)

        if self._mouse_pressed:
            vector = event.pos() - self._mouse_position
            if self.resizing:
                rect = self.geometry()
                offset = self.mapToParent(self._mouse_position + vector)
                resize_area = self._resize_area.lower()
                if 'left' in resize_area:
                    new_width = rect.width() + rect.left() - offset.x()
                    if new_width > self.minimumWidth():
                        rect.setLeft(offset.x())
                if 'top' in resize_area:
                    new_height = rect.height() + rect.top() - offset.y()
                    if new_height > self.minimumHeight():
                        rect.setTop(offset.y())
                if 'right' in resize_area:
                    rect.setRight(offset.x())
                if 'bottom' in resize_area:
                    rect.setBottom(offset.y())
                self.setGeometry(rect)
            else:
                self.move(self.mapToParent(vector))

    def mouseReleaseEvent(self, event):
        self._mouse_pressed = False
        self._mouse_position = None

    def minimumSizeHint(self):
        return QtCore.QSize(640, 480)
