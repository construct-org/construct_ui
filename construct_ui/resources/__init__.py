# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
import re
import glob
import logging

from construct.utils import unipath
from construct_ui.utils import get_scale_factor


_log = logging.getLogger('construct.ui.resources')
THIS_PATH = unipath(os.path.dirname(__file__))
EXTENSIONS = ['', '.png', '.ttf', '.css']
PATTERNS = [unipath(THIS_PATH, 'icons', '*.png')]
ICON_EXT = '.png'
ICONS_GLOB = unipath(THIS_PATH, 'icons', '*' + ICON_EXT)
STYLE_EXT = '.css'
STYLES_GLOB = unipath(THIS_PATH, 'styles', '*' + STYLE_EXT)
FONT_EXT = '.ttf'
FONTS_GLOB = unipath(THIS_PATH, 'fonts', '*' + FONT_EXT)


class ResourceError(Exception):
    pass


def style(resource, scale_factor=None):
    '''Get a stylesheet'''

    scale_factor = scale_factor or get_scale_factor()
    style = read(resource)
    pixel_values = re.findall(r'\d+px', style)
    for pixel_value in pixel_values:
        value = str(int(int(pixel_value[:-2]) * scale_factor)) + 'px'
        style.replace(pixel_value, value, 1)
    return style


def read(resource):
    '''Read a resource'''

    resource_path = path(resource)
    with open(resource_path, 'rb') as f:
        return f.read()


def path(resource):
    '''Get a resources filepath'''

    filepath = resource.lstrip(':/')
    for ext in EXTENSIONS:
        potential_path = unipath(THIS_PATH, filepath + ext)
        if os.path.isfile(potential_path):
            return potential_path
    raise ResourceError('Could not find resource: ' + resource)


def list(search=None):
    '''List all resources'''

    def is_match(resource_path):
        return not search or search in resource_path

    resources = []
    for ext in EXTENSIONS[1:]:
        pattern = unipath(THIS_PATH, '*', '*' + ext)
        for filepath in glob.glob(pattern):
            root = os.path.basename(os.path.dirname(filepath))
            basename = os.path.basename(filepath)
            name, ext = os.path.splitext(basename)
            resource_path = ':/' + root + '/' + name
            if is_match(resource_path):
                resources.append(resource_path)

    return resources


def preview_icons():
    '''Show an icon preview dialog'''

    from Qt import QtWidgets
    from construct_ui.widgets import IconButton

    app = QtWidgets.QApplication.instance()
    standalone = False
    if not app:
        standalone = True
        app = QtWidgets.QApplication([])
        init()

    clipboard = app.clipboard()
    dialog = QtWidgets.QDialog()
    layout = QtWidgets.QGridLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)
    columns = 3
    for i, resource_path in enumerate(list('icons')):
        icon = IconButton(resource_path)
        label = QtWidgets.QLabel(resource_path)
        copy = lambda: clipboard.setText(resource_path)
        icon.clicked.connect(copy, strong=True)
        for r in icon.clicked.receivers._refs:
            print(r)
        col, row = (i % columns) * 2, int(i * (1.0 / float(columns)))
        layout.addWidget(icon, row, col)
        layout.addWidget(label, row, col + 1)

    dialog.setLayout(layout)
    dialog.setStyleSheet(style(':/styles/dark'))

    if standalone:
        dialog.exec_()


def qfile(resource):
    '''Get a resource as a QFile'''

    from Qt import QtGui
    return QtGui.QFile(resource)


def qicon(resource, use_cache=True, cache={}):
    '''Get a resource as a QIcon'''

    if use_cache and resource in cache:
        return cache[resource]

    from Qt import QtGui
    pixmap = qpixmap(resource, use_cache)
    icon = QtGui.QIcon(pixmap)
    cache[resource] = icon
    return icon


def qpixmap(resource, use_cache=True, cache={}):
    '''Get a resource as a QPixmap'''

    if use_cache and resource in cache:
        return cache[resource]

    from Qt import QtGui
    scale = get_scale_factor()
    xform = QtGui.QTransform()
    xform.scale(scale, scale)
    pixmap = QtGui.QPixmap(resource).transformed(xform)
    cache[resource] = pixmap
    return pixmap


def init():
    '''Initialize resources and fonts'''
    from construct_ui import _resources
    from Qt import QtGui
    for resource_path in list('fonts'):
        font_path = path(resource_path)
        QtGui.QFontDatabase.addApplicationFont(font_path)
