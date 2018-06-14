# -*- coding: utf-8 -*-
from __future__ import absolute_import
import inspect
from abc import ABCMeta


ABC = ABCMeta('ABC', (object,), {})


class ABCNonMeta(object):
    '''ABCMeta can not be used as a mixin with Qt classes, this is an
    alternative implementation that is NOT a metaclass. The __new__ method
    validates a subclass only the first time it is instanced. If the subclass
    passes validation, we set __concrete__ to True, if the subclass does not
    match the ABC interface, a TypeError is raised and __concrete__ is set
    to False. Future instances of the subclass do not perform the validation,
    they just check the value of __concrete__, minimizing performance costs.
    '''

    __concrete__ = None
    __abstracts__ = None

    def __new__(cls, *args, **kwargs):
        if cls.__concrete__ is None:
            cls.__abstracts__ = {}
            for name, member in inspect.getmembers(cls):
                if getattr(member, '__isabstractmethod__', False):
                    cls.__abstracts__[name] = member
            cls.__concrete__ = not cls.__abstracts__

        if not cls.__concrete__:
            raise TypeError((
                "Can't instantiate abstract class {} with abstract methods {}"
            ).format(
                cls.__name__,
                ', '.join(cls.__abstracts__)
            ))

        return super(ABCNonMeta, cls).__new__(cls, *args, **kwargs)


def is_implemented(obj):
    '''Returns True if an object does not have an attr "not_implemented"

    See also:
        :func:`not_implemented`'''

    return not hasattr(obj, 'not_implemented')


def not_implemented(obj):
    '''Sets an attribute "not_implemented" to True on the given obj'''

    obj.not_implemented = True
    return obj


def get_dpi():
    '''Get screen DPI. Use to scale UI independent of monitor size.'''

    from Qt import QtWidgets

    app = QtWidgets.QApplication.instance()
    if app:
        return float(app.desktop().logicalDpiX())
    return 96.0


def get_scale_factor(factor=[]):
    '''Get scale factor for icons'''

    if not factor:
        factor.append(get_dpi() / 96.0)
    return factor[0]
