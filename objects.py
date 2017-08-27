
class Base(object):
    def value(self):
        return None

class Return(Base):
    def __init__(self,  value):
        self.value = value
    def value(self):
        return self.value
        
    
