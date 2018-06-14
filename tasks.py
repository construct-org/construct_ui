#!/usr/bin/env
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
import os
from invoke import task


def norm_path(*parts):
    return os.path.join(*parts).replace('\\', '/')


def rel_path(*parts):
    return norm_path(*parts)


def rcc_cmd():
    from Qt import _QtGui
    qtdir = os.path.dirname(_QtGui.__file__)
    potential_names = [
        'pyrcc4', 'pyrcc4.exe', 'pyrcc4.bat',  # PyQt4
        'pyrcc5', 'pyrcc5.exe', 'pyrcc5.bat',  # PyQt5
        'pyside-rcc', 'pyside-rcc.exe',  # PySide
    ]
    for name in potential_names:
        potential_path = rel_path(qtdir, name)
        if os.path.isfile(potential_path):
            return potential_path

    raise OSError('Could not find qt rcc...')


PYSIDE_PATH = os.path.expandvars('$VIRTUAL_ENV/lib/site-packages/PySide/')
SCSS_SRC = rel_path('construct_ui', 'resources', 'scss')
CSS_BLD = rel_path('construct_ui', 'resources', 'styles')
QTSASS_CMD = 'qtsass %s -o %s' % (SCSS_SRC, CSS_BLD)
QRC_SRC = rel_path('resources.qrc')
QRC_BLD = rel_path('construct_ui', '_resources.py')
QRC_CMD = (rcc_cmd() + ' %s -o %s') % (QRC_SRC, QRC_BLD)
QRC_TMPL = '''
<!DOCTYPE RCC><RCC version="1.0">
<qresource>
{}
</qresource>
</RCC>
'''
QRC_FILE_TMPL = '    <file alias="{alias}">{path}</file>'
ICON_EXT = '.png'
ICONS_PATH = rel_path('construct_ui', 'resources', 'icons')
STYLE_EXT = '.css'
STYLES_PATH = rel_path('construct_ui', 'resources', 'styles')


def patch_qrcpy(resource):
    '''Patch qrcpy file'''

    import Qt

    with open(resource, 'r') as f:
        contents = f.read()

    # Patch imports
    contents = contents.replace(Qt.__binding__, 'Qt')

    with open(resource, 'w') as f:
        f.write(contents)


def generate_qrc():
    '''Generate qrc file'''

    lines = []

    for file in os.listdir(ICONS_PATH):
        name, ext = os.path.splitext(file)
        if ext != ICON_EXT:
            continue

        line = QRC_FILE_TMPL.format(
            alias=norm_path('icons', name),
            path=norm_path(ICONS_PATH, file)
        )
        lines.append(line)

    for file in os.listdir(STYLES_PATH):
        name, ext = os.path.splitext(file)
        if ext != STYLE_EXT:
            continue

        line = QRC_FILE_TMPL.format(
            alias=norm_path('styles', name),
            path=norm_path(STYLES_PATH, file)
        )
        lines.append(line)

    return QRC_TMPL.format('\n'.join(lines))


@task
def build_css(ctx):
    '''Build stylesheets'''

    ctx.run(QTSASS_CMD)


@task
def build_qrc(ctx):
    '''Build qresources'''

    text = generate_qrc()
    with open(QRC_SRC, 'w') as f:
        f.write(text)

    ctx.run(QRC_CMD)
    patch_qrcpy(QRC_BLD)

    os.remove(QRC_SRC)


@task
def build(ctx):
    '''Build all resources'''

    build_css(ctx)
    build_qrc(ctx)


@task
def develop(ctx):
    '''Build and watch resources'''

    ctx.run(QTSASS_CMD + ' -w')
