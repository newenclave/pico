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

