# -*- coding: utf-8 -*-
from __future__ import absolute_import

from construct_ui.widgets.icons import DropDownIcon
from construct_ui.widgets.labels import Label

from Qt import QtWidgets, QtCore


class CollapsableList(QtWidgets.QWidget):

    def __init__(self, label, parent=None):
        super(CollapsableList, self).__init__(parent=parent)
        self.default_label = label

        self.drop_down_button = DropDownIcon(parent=self)
        self.drop_down_button.toggled.connect(self.on_toggled)
        self.drop_down_button.setEnabled(True)
        self.label = Label(self.default_label)
        self.label.clicked.connect(self.drop_down_button.toggle)
        self.header_layout = QtWidgets.QHBoxLayout()
        self.header_layout.setSpacing(0)
        self.header_layout.addWidget(self.drop_down_button)
        self.header_layout.addWidget(self.label)
        self.header_layout.addStretch()

        self.list_widget = QtWidgets.QListWidget()
        self.list_widget.itemDoubleClicked.connect(
            self.drop_down_button.toggle
        )
        self.list_widget.setHidden(False)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.layout.setSpacing(0)
        self.layout.addLayout(self.header_layout, 0)
        self.layout.addWidget(self.list_widget, 1)
        self.layout.addStretch()

        self.setLayout(self.layout)
        self.setAttribute(QtCore.Qt.WA_StyledBackground)

    def on_toggled(self, value):
        self.list_widget.setVisible(value)
        if value:
            self.label.setText(self.default_label)
        else:
            item = self.list_widget.currentItem()
            if item:
                self.label.setText(item.text())
