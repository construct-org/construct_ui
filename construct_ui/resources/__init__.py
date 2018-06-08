# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
import glob
from construct.utils import unipath
from construct_ui import _resources


THIS_PATH = unipath(os.path.dirname(__file__))
ICON_EXT = '.png'
ICONS_GLOB = unipath(THIS_PATH, 'icons', '*' + ICON_EXT)
STYLE_EXT = '.css'
STYLES_GLOB = unipath(THIS_PATH, 'styles', '*' + STYLE_EXT)
CACHE = {}


class ResourceError(Exception):
    pass


def read(resource):
    '''Read a resource'''

    resource_path = path(resource)
    with open(resource_path, 'r') as f:
        return f.read()


def path(resource):
    '''Get a resources filepath'''

    if resource.startswith(':/icons'):
        potential_path = unipath(THIS_PATH, resource.lstrip(':/') + ICON_EXT)
        if not os.path.isfile(potential_path):
            raise ResourceError('Could not find resource: ' + resource)
        return potential_path

    if resource.startswith(':/styles'):
        potential_path = unipath(THIS_PATH, resource.lstrip(':/') + STYLE_EXT)
        if not os.path.isfile(potential_path):
            raise ResourceError('Could not find resource: ' + resource)
        return potential_path


def list():
    '''List all resources'''

    resources = []

    for filepath in glob.glob(ICONS_GLOB):
        filepath = unipath(filepath)
        basename = os.path.basename(filepath)
        name, ext = os.path.splitext(basename)
        resources.append(':/icons/' + name)

    for filepath in glob.glob(STYLES_GLOB):
        filepath = unipath(filepath)
        basename = os.path.basename(filepath)
        name, ext = os.path.splitext(basename)
        resources.append(':/styles/' + name)


def qfile(resource):
    '''Get a resource as a QFile'''

    from Qt import QtGui
    return QtGui.QFile(resource)


def qicon(resource):
    '''Get a resource as a QIcon'''

    from Qt import QtGui
    return QtGui.QIcon(resource)


def qpixmap(resource):
    '''Get a resource as a QPixmap'''

    from Qt import QtGui
    return QtGui.QPixmap(resource)
