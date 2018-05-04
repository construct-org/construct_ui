#!/usr/bin/env
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
import os
from invoke import task

scss_src = 'construct_ui/resources/scss'
css_build = '../css'


def build_scss_cmds(watch=False):
    cmds = []
    for f in os.listdir(scss_src):
        if f.endswith('.scss') and not f.startswith('_'):
            src = f
            bld = css_build + '/' + f.replace('.scss', '.css')
            cmd = 'qtsass %s -o %s%s' % (src, bld, ' -w' if watch else '')
            cmds.append(cmd)
    return cmds


@task
def build(ctx, watch=False):
    '''Build resources - scss'''
    import subprocess
    procs = [
        subprocess.Popen(cmd.split(), cwd=scss_src)
        for cmd in build_scss_cmds(watch)
    ]
    for p in procs:
        p.wait()
