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
        self.clear()
        self.create()

    def create(self, groups=None, parent=None):

        if not groups:
            groups = group_actions(construct.actions.collect())
            parent = self

        for group, actions in groups.items():
            if group == '':
                for action in actions:
                    qaction = self._create_action(action, parent)
                    parent.addAction(qaction)
            else:
                submenu = QtWidgets.QMenu(group.title(), parent)
                parent.addMenu(submenu)
                self.create(actions, submenu)

    def _create_action(self, action, parent):
        '''Creates a QAction from a Construct Action'''

        def _run_action():
            action().run()

        qaction = QtWidgets.QAction(action.label, parent)
        qaction.triggered.connect(_run_action)
        return qaction



def main():
    import sys
    import construct
    construct.init()
    construct.set_context_from_path(
        'C:/Users/danie/projects/faux/assets/product/coffee/model/work/maya'
    )
    app = QtWidgets.QApplication([])
    win = QtWidgets.QMainWindow()
    bar = win.menuBar()
    bar.addMenu(ActionMenu('Actions', win))
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
