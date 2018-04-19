# -*- coding: utf-8 -*-
from __future__ import absolute_import
import construct
from construct.action import group_actions
from Qt import QtWidgets


class ActionMenu(QtWidgets.QMenu):
    '''Menu generated from a Context. Presents all available Actions as
    qmenu actions organized by Action identifier.
    '''

    def __init__(self, name, parent=None):
        super(ActionMenu, self).__init__(name, parent)
        self.aboutToShow.connect(self.before_show)

    def before_show(self):
        create_action_menu(parent=self)


def create_action_menu(groups=None, parent=None):
    '''Decoupled from ActionMenu class so we can use it with Maya directly'''

    if groups is None:
        groups = group_actions(construct.actions.collect())
        parent.clear()

    for group, actions in groups.items():
        if group == '':
            for action in actions:
                qaction = create_action_menu_item(action, parent)
                parent.addAction(qaction)
        else:
            submenu = QtWidgets.QMenu(group.title(), parent)
            parent.addMenu(submenu)
            create_action_menu(actions, submenu)


def create_action_menu_item(action, parent):
    '''Creates a QAction from a Construct Action'''

    def run_action():
        action().run()

    qaction = QtWidgets.QAction(action.label, parent)
    qaction.triggered.connect(run_action)
    return qaction
