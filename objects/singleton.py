#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 07:04:56 2020
Ce programme analyse et crée un rapport financier
@author: romain Boyrie
"""
from weakref import WeakValueDictionary


class SingletonType(type):
    _instances = WeakValueDictionary()
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super(SingletonType, cls).__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
