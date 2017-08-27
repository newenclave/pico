import astree

class Walker(object):
    def __init__(self,  ast,  env):
        self.ast = ast
        self.env = env
    
    def eval_scope(self,  scope):
        pass
        
    def eval_next(self, node):
        if isinstance(node, astree.Scope):
            self.eval_scope(node)
        
    def eval(self):
        pass
