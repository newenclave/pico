import objects

class BuiltinError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return 'builtin error: ' + repr(self.value)

class Len(objects.Builtin):
    def __init__(self, env):
        super(Len, self).__init__(env)
    def call(self, params):
        if len(params) < 1:
            raise BuiltinError('len call with empty paramenets')
        return objects.Number(len(params[0].value( )))

class Print(objects.Builtin):
    def __init__(self, env):
        super(Print, self).__init__(env)
    def call(self, params):
        for i in params:
            print( i, ' ',  end='' )
        print()
