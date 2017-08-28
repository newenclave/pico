
class Type:
    NONE     = 'null'
    INTEGER  = 'int'
    STRING   = 'string'
    BOOLEAN  = 'bool'
    ARRAY    = 'array'
    TABLE    = 'table'
    FUNCTION = 'function'
    BUILTIN  = 'builtin'

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
    def __hash__(self):
        return hash(self.value( ))
    def __eq__(self, other):
        return (self.type( ) == other.type( )) \
           and (self.value( ) == other.value( ))
    def __ne__(self, other):
        return not(self == other)

class String(Base):
    def __init__(self,  value):
        self.val = value
    def value(self):
        return self.val
    def __str__(self):
        return '"{0}"'.format(self.val)
    def type(self):
        return Type.STRING
    def __hash__(self):
        return hash(self.value( ))
    def __eq__(self, other):
        return (self.type( ) == other.type( )) \
           and (self.value( ) == other.value( ))
    def __ne__(self, other):
        return not(self == other)

class Boolean(Base):
    def __init__(self,  value):
        self.val = value
    def value(self):
        return self.val
    def __str__(self):
        return 'true' if self.val else 'false'
    def type(self):
        return Type.BOOLEAN
    def __hash__(self):
        return hash(self.value( ))
    def __eq__(self, other):
        return (self.type( ) == other.type( )) \
           and (self.value( ) == other.value( ))
    def __ne__(self, other):
        return not(self == other)

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
    def __eq__(self, other):
        return (self.type( ) == other.type( )) \
           and (self.value( ) == other.value( ))
    def __ne__(self, other):
        return not(self == other)

class Table(Base):
    def __init__(self, value):
        self.val = value
    def value(self):
        return self.val
    def __str__(self):
        res = '{'
        size = 0
        for k in self.val:
            res += '{0}: {1}'.format( str(k), str(self.val[k]))
            size += 1
            if size != len(self.val):
                res += ', '
        res += '}'
        return res
    def type(self):
        return Type.TABLE
    def __eq__(self, other):
        return (self.type( ) == other.type( )) \
           and (self.value( ) == other.value( ))
    def __ne__(self, other):
        return not(self == other)

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

class Builtin(Base):

    def __init__(self, env):
        self.environ = env
    def env(self):
        return self.environ

    def call(self,  params):
        pass

    def __str__(self):
        return '<builtin>'
    def type(self):
        return Type.BUILTIN


