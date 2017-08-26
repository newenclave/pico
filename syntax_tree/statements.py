from . import node

class Let(node.Node):
    def __init__(self,  ident,  expr):
        self.ident = ident
        self.expr  = expr
    def __str__(self):
        return 'let {0} = {1}'.format(self.ident, self.expr)

class Return(node.Node):
    def __init__(self,  expr):
        self.expr  = expr
    def __str__(self):
        return 'return {0}'.format(self.expr)

