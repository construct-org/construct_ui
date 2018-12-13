# -*- coding: utf-8 -*-
from __future__ import absolute_import

from Qt import QtWidgets, QtCore, QtCompat

import construct
from construct_ui.views.view import View
from construct_ui.controls.query_list_control import QueryListControl


class Navigation(View, QtWidgets.QWidget):

    def create(self):
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setAlignment(QtCore.Qt.AlignTop)

        project_query = construct.search(
            root=self.data.root,
            tags=['project'],
            depth=1
        )

        self.project_list = QueryListControl(
            'Projects',
            project_query,
            formatter=lambda entry: entry.name,
            parent=self
        )

    def update(self):
        pass
