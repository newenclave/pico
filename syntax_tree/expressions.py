from . import node

class Ident(node.Node):
    def __init__(self,  name):
        self.val = name

    def value(self):
        return self.val

    def __str__(self):
        return self.val

class String(node.Node):
    def __init__(self, val):
        self.val = val

    def value(self):
        return self.val

    def __str__(self):
        return '"{0}"'.format(self.val)

class Number(node.Node):
    def __init__(self, val):
        self.val = val

    def value(self):
        return self.val

    def __str__(self):
        return '{0}'.format(self.val)

class Bool(node.Node):
    def __init__(self, val):
        self.val = val

    def value(self):
        return self.val

    def __str__(self):
        return '{0}'.format('true' if self.val else 'false')

class Prefix(node.Node):
    def __init__(self, oper,  expr):
        self.oper = oper
        self.expr = expr
    def __str__(self):
        return '({0}{1})'.format( self.oper, self.expr )

class Infix(node.Node):
    def __init__(self, oper, left, right):
        self.oper = oper
        self.left = left
        self.right = right
    def __str__(self):
        return '({0}{1}{2})'.format( self.left,  self.oper, self.right )

class Function(node.Node):
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
        res += ') {\n'
        for i in self.body:
            res = res + str(i) + ';\n'
        res = res + '}'
        return res
    
class IfElse(node.Node):
    def __init__(self,  cond, body,  altbody):
        self.cond    = cond
        self.body    = body
        self.altbody = altbody
    def __str__(self):  
        res = 'if(' + str(self.cond) + ') {\n'
        for i in self.body:
            res += str(i)
            res += ';\n'
        res += '} '
        if len(self.altbody) > 0:
            res += 'else {\n'
            for i in self.altbody:
                res += str(i)
                res += ';\n'
            res += '} '
        return res
        
class Call(node.Node):
    def __init__(self, obj,  params, body):        
        self.obj     = obj
        self.params  = params
        self.body    = body
    def __str__(self):
        res = str(self.obj) + '('
        size = 0
        for i in self.idents:
            res += str(i)
            size += 1
            if size != len(self.idents): 
                res += ', '
        res += ') {\n'
        for i in self.body:
            res = res + str(i) + ';\n'
        res = res + '}'
        return res

