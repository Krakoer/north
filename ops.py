from enum import auto, Enum


class Ops(Enum):
    PUSH=auto()
    PLUS=auto()
    DUMP=auto()
    MINUS = auto()
    EQUAL = auto()
    IF = auto()
    END = auto()
    ELSE = auto()
    GT = auto()
    LT = auto()
    DUP = auto()
    WHILE = auto()
    DO = auto()
    MEM = auto()

def push():
    return Ops.PUSH

def plus():
    return Ops.PLUS

def dump():
    return Ops.DUMP

def minus():
    return Ops.MINUS

def equal():
    return Ops.EQUAL

def iff():
    return Ops.IF

def elze():
    return Ops.ELSE

def end():
    return Ops.END

def greater():
    return Ops.GT

def less():
    return Ops.LT

def dup():
    return Ops.DUP

def wile():
    return Ops.WHILE

def do():
    return Ops.DO

def mem():
    return Ops.MEM