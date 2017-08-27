
class Environment(object):
    def __init__(self, parent = None):
        self.values = { }
        self.parent = parent
        
    def set(self,  key,  value):
        self.values[key] = value
        
    def get(self,  key):
        tmp = self
        while tmp:
            if key in tmp.values:
                return tmp.values[key]
            elif tmp.parent:
                tmp = tmp.parent
            else:
                tmp = None
        return None
        
