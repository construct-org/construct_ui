# -*- coding: utf-8 -*-
from __future__ import absolute_import
from inspect import getmembers


class StyledProperty(object):

    def __init__(self, name, default):
        self.name = name
        self.default = default

    def __get__(self, obj, typ):
        if not obj:
            return self

        # Get prop value from cache
        obj.__dict__.setdefault('_properties', {})
        return obj._properties.setdefault(self.name, self.default)

    def __set__(self, obj, value):

        # Update prop cache
        obj.__dict__.setdefault('_properties', {})
        obj._properties[self.name] = value

        # Refresh widget style
        obj.setProperty(self.name, value)
        obj.setStyle(obj.style())

    @staticmethod
    def init(obj):
        '''Initialize properties...call in __init__ method of a class that has
        StyledProperties.'''

        for _, prop in getmembers(obj, lambda x: isinstance(x, StyledProperty)):
            print(prop, prop.name, prop.default)
            obj.__dict__.setdefault('_properties', {})
            obj._properties.setdefault(prop.name, prop.default)
            obj.setProperty(prop.name, prop.default)
            obj.setStyle(obj.style())
