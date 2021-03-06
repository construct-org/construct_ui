# -*- coding: utf-8 -*-
from __future__ import absolute_import
import logging
import traceback
import construct
from construct.action import group_actions
from construct_ui import resources
from Qt import QtWidgets


_log = logging.getLogger('construct.menus')


class ActionMenu(QtWidgets.QMenu):
    '''Menu generated from the current context. Presents all available Actions
    grouped by Action identifier. For example all Actions with identifiers
    matching launch.* will appear in a submenu named Launch.
    '''

    def __init__(self, name, parent=None):
        super(ActionMenu, self).__init__(name, parent)
        self.aboutToShow.connect(self.before_show)

    def before_show(self):
        create_action_menu(parent=self)


def create_action_menu(groups=None, parent=None):
    '''Decoupled from ActionMenu class so we can use it with existing menus'''

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

    def menu_action():
        '''Attempts to create a form for the menu item's Action. If no form is
        available, just run the action.
        '''

        try:
            construct.show_form(action.identifier)
        except Exception as e:
            _log.error('Failed to show ActionForm: %s', str(e))
            traceback.print_exc()
            action().run()

    qaction = QtWidgets.QAction(action.label, parent)
    qaction.triggered.connect(menu_action)
    return qaction
