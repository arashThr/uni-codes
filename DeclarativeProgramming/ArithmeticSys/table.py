# Implementation of table which holds functions for operation
# Table definition: A dictionary filled with functions
_table = dict()
def put(op, opType, item):
    _table[op, opType] = item
def get(op, opType):
    return _table[op, opType]

