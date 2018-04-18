# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
from construct.utils import unipath


this_folder = unipath(os.path.dirname(__file__))


def styles():
    '''Get a dict containing all stylesheets'''

    data = {}
    root = unipath(this_folder, 'css')
    for f in os.listdir(root):
        path = unipath(root, f)
        if os.path.isfile(path):
            name = os.path.splitext(f)[0]
            data[name] = path
    return data


def style(name):
    '''Get the fullpath of a stylesheet by name'''

    try:
        return styles()[name]
    except KeyError:
        raise KeyError('Could not find style: %s' % name)


def icons():
    '''Get a dict containing all icons'''

    data = {}
    root = unipath(this_folder, 'icons')
    for f in os.listdir(root):
        path = unipath(root, f)
        if os.path.isfile(path):
            name = os.path.splitext(f)[0]
            data[name] = path
    return data


def icon(name):
    '''Get the fullpath of an icon by name'''

    try:
        return icons()[name]
    except KeyError:
        raise KeyError('Could not find icon: %s' % name)
