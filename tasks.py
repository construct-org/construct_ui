#!/usr/bin/env
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
import os
from subprocess import Popen
from invoke import task


def norm_path(*parts):
    return os.path.join(*parts).replace('\\', '/')


def rel_path(*parts):
    return norm_path(*parts)

PYSIDE_PATH = os.path.expandvars('$VIRTUAL_ENV/lib/site-packages/PySide/')
SCSS_SRC = rel_path('construct_ui', 'resources', 'scss')
CSS_BLD = rel_path('construct_ui', 'resources', 'css')
QTSASS_CMD = 'qtsass %s -o %s' % (SCSS_SRC, CSS_BLD)
QRC_SRC = rel_path('resources.qrc')
QRC_BLD = rel_path('construct_ui', '_resources.py')
QRC_CMD = (PYSIDE_PATH + 'pyside-rcc %s -o %s') % (QRC_SRC, QRC_BLD)
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
def build_qrc(ctx):
    '''Build qresources'''

    text = generate_qrc()
    with open(QRC_SRC, 'w') as f:
        f.write(text)

    p = Popen(QRC_CMD.split())
    p.wait()


@task
def build(ctx):
    '''Build resources - scss'''

    p = Popen(QTSASS_CMD.split())
    p.wait()


@task
def develop(ctx):
    '''Build and watch resources - scss'''

    p = Popen(QTSASS_CMD.split() + ['-w'])
    p.wait()
