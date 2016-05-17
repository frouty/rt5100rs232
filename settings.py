# -*- coding: utf-8 -*-
def constant(f):
    def fset(self, value):
        raise SyntaxError
    def fget(self):
        return f()
    return property(fget, fset)

class _Const(object):
    """START must be the lowest number 
    minus if there is minus"""
    @constant
    def START_SPH():
        return -20
    @constant
    def STOP_SPH():
        return 20
    @constant
    def STEP_SPH():
        return 0.25
    @constant
    def START_AXIS():
        return 0
    @constant
    def STOP_AXIS():
        return 175
    @constant
    def STEP_AXIS():
        return 5
    @constant
    def START_CYL():
        return -8.75
    @constant
    def STOP_CYL():
        return 0
    @constant
    def STEP_CYL():
        return 0.25

CONST = _Const()
# #import settings
# #settings.CONST.START
