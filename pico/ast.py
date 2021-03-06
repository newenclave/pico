
class Node(object):
    def value(self):
        return None

class Let(Node):
    def __init__(self,  ident,  expr):
        self.ident = ident
        self.expr  = expr
    def __str__(self):
        return 'let {0} = {1}'.format(self.ident, self.expr)

class Return(Node):
    def __init__(self,  expr):
        self.expr = expr
    def value(self):
        return self.expr
    def __str__(self):
        return 'return {0}'.format(self.expr)

class Scope(Node):
    def __init__(self,  stmt):
        self.stmt = stmt

    def value(self):
        return self.stmt

    def __str__(self):
        res = '{\n'
        for i in self.stmt:
            res += (str(i) + ';\n')
        res += '}'
        return res;

class Ident(Node):
    def __init__(self, name):
        self.name = name

    def value(self):
        return self.name

    def __str__(self):
        return self.name

class String(Node):
    def __init__(self, val):
        self.val = val

    def value(self):
        return self.val

    def __str__(self):
        return '"{0}"'.format(self.val)

class Number(Node):
    def __init__(self, val):
        self.val = val

    def value(self):
        return self.val

    def __str__(self):
        return '{0}'.format(self.val)

class Boolean(Node):
    def __init__(self, val):
        self.val = val

    def value(self):
        return self.val

    def __str__(self):
        return '{0}'.format('true' if self.val else 'false')

class Prefix(Node):
    def __init__(self, oper,  expr):
        self.oper = oper
        self.expr = expr
    def value(self):
        return self.expr

    def operator(self):
        return self.oper

    def __str__(self):
        return '({0}{1})'.format( self.oper, self.expr )

class Infix(Node):
    def __init__(self, oper, left, right):
        self.oper = oper
        self.lft = left
        self.rght = right

    def left(self):
        return self.lft

    def right(self):
        return self.rght

    def operator(self):
        return self.oper

    def __str__(self):
        return '({0}{1}{2})'.format( self.left(), self.oper, self.right() )

class Function(Node):
    def __init__(self,  idents,  body):
        self.idents = idents
        self.body   = body
    def __str__(self):
        res = 'fn('
        size = 0
        for i in self.idents:
            res += str(i)
            size += 1
            if size != len(self.idents):
                res += ', '
        res += ') '
        res += self.body
        
        return res

class IfElse(Node):
    def __init__(self,  cond, body,  altbody):
        self._cond    = cond
        self._body    = body
        self._altbody = altbody

    def cond(self):
        return self._cond
    def body(self):
        return self._body
    def alt(self):
        return self._altbody

    def __str__(self):
        res = 'if(' + str(self._cond) + ') '
        res += self._body
        if len(self._altbody.value( )) > 0:
            res += 'else '
            res += self._altbody
        return res

class Call(Node):
    def __init__(self, obj,  params):
        self.obj     = obj
        self.param   = params
    def value(self):
        return self.obj

    def params(self):
        return self.param

    def __str__(self):
        res = str(self.obj) + '('
        size = 0
        for i in self.param:
            res += str(i)
            size += 1
            if size != len(self.param):
                res += ', '
        res += ')'
        return res

class Array(Node):
    def __init__(self, expr):
        self.expr     = expr

    def value(self):
        return self.expr

    def __str__(self):
        res = '['
        size = 0
        for i in self.expr:
            res += str(i)
            size += 1
            if size != len(self.expr):
                res += ', '
        res += ']'
        return res

class Table(Node):
    def __init__(self, expr):
        self.expr     = expr

    def value(self):
        return self.expr

    def __str__(self):
        res = '{'
        size = 0
        for i in self.expr:
            res += '{0}:{1}'.format(str(i[0]),  str(i[1]))
            size += 1
            if size != len(self.expr):
                res += ', '
        res += '}'
        return res

class Index(Node):
    def __init__(self, obj,  param):
        self.obj     = obj
        self.param   = param

    def value(self):
        return self.obj

    def index(self):
        return self.param

    def __str__(self):
        res = str(self.obj) + '[' + str(self.param) + ']'
        return res


