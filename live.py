# -*- coding: utf-8 -*-
'''Live CSS Reloading for PySide'''

from Qt import QtCore
from collections import defaultdict


class LiveStyle(QtCore.QFileSystemWatcher):
    '''Updates a widgets style when its css changes.

    Simple usage:

        w = QtGui.QWidget()
        LiveStyle(path='path/to/style.css', parent=w)

    Multiple widgets and stylesheets:

        w = QtGui.QMainWindow()
        d = QtGui.QDialog(parent=w)

        live = LiveStyle(parent=w)
        live.link(w, 'path/to/windowstyle.css')
        live.link(d, 'path/to/dialogstyle.css')

    '''

    def __init__(self, path=None, parent=None):
        super(LiveStyle, self).__init__(parent)
        self.fileChanged.connect(self.css_changed)
        self.path_mapping = defaultdict(set)

        if path and parent:
            self.link(parent, path)

    def __repr__(self):
        return '<{}>(parent={})'.format(self.__class__.__name__, self.parent())

    def link(self, widget, path):
        '''Links a widget to a stylesheet path.

        Arguments:
            widget: QtGui.QWidget instance
            path: Filepath to stylesheet
        '''

        self.path_mapping[path].add(widget)
        self.addPath(path)

    def unlink(self, widget, path):
        '''Unlinks a widget from a stylesheet path.

        Arguments:
            widget: QtGui.QWidget instance
            path: Filepath to stylesheet
        '''

        if not self.path_mapping[path]:
            return

        self.path_mapping[path].discard(widget)
        if not self.path_mapping[path]:
            self.path_mapping.pop(path)
            self.removePath(path)

    def css_changed(self, path):
        '''Updates all widget linked to the changed filepath.'''

        widgets = self.path_mapping[path]
        with open(path) as f:
            style = f.read()
            for widget in widgets:
                widget.style().unpolish(widget)
                widget.setStyleSheet(style)
                widget.style().polish(widget)
