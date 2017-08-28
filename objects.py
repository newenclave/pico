
class Type:
    NONE     = 'null'
    INTEGER  = 'int'
    STRING   = 'string'
    BOOLEAN  = 'bool'
    ARRAY    = 'array'
    FUNCTION = 'function'

class Base(object):
    def value(self):
        return None
    def type(self):
        return Type.NONE

class Return(Base):
    def __init__(self,  value):
        self.val = value
    def value(self):
        return self.val

class Number(Base):
    def __init__(self,  value):
        self.val = value
    def value(self):
        return self.val
    def __str__(self):
        return str(self.val)
    def type(self):
        return Type.INTEGER

class String(Base):
    def __init__(self,  value):
        self.val = value
    def value(self):
        return self.val
    def __str__(self):
        return '"{0}"'.format(self.val)
    def type(self):
        return Type.STRING

class Boolean(Base):
    def __init__(self,  value):
        self.val = value
    def value(self):
        return self.val
    def __str__(self):
        return 'true' if self.val else 'false'
    def type(self):
        return Type.BOOLEAN

class Array(Base):
    def __init__(self, value):
        self.val = value
    def value(self):
        return self.val
    def __str__(self):
        res = '['
        size = 0
        for i in self.val:
            res += str(i)
            size += 1
            if size != len(self.val):
                res += ', '
        res += ']'
        return res
    def type(self):
        return Type.ARRAY

class Function(Base):
    def __init__(self, idents, body,  env):
        self.idents  = idents
        self.scope   = body
        self.environ = env

    def params(self):
        return self.idents

    def body(self):
        return self.scope

    def env(self):
        return self.environ

    def __str__(self):
        return '<function>'
    def type(self):
        return Type.FUNCTION


