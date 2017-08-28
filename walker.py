import astree
import environment
import objects
import tokens

class ExecutionError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return 'execution error: ' + repr(self.value)

class Walker(object):

    def __init__(self, ast, env = None):
        self.ast = ast
        self.env = env if env else environment.Environment( )

        self.oper_prefix = {
            (tokens.BANG['name'],  objects.Type.BOOLEAN): objects.Type.BOOLEAN,
            (tokens.MINUS['name'], objects.Type.INTEGER): objects.Type.INTEGER,
        }

        self.oper_infix = {
            (objects.Type.INTEGER, tokens.MINUS['name'],    objects.Type.INTEGER):  objects.Type.INTEGER,

            (objects.Type.INTEGER, tokens.PLUS['name'],     objects.Type.INTEGER):  objects.Type.INTEGER,
            (objects.Type.STRING,  tokens.PLUS['name'],     objects.Type.STRING):   objects.Type.STRING,
            (objects.Type.ARRAY,   tokens.PLUS['name'],     objects.Type.ARRAY):    objects.Type.ARRAY,

            (objects.Type.INTEGER, tokens.ASTERISK['name'], objects.Type.INTEGER):  objects.Type.INTEGER,

            (objects.Type.INTEGER, tokens.SLASH['name'],    objects.Type.INTEGER):  objects.Type.INTEGER,

            (objects.Type.INTEGER, tokens.EQ['name'],       objects.Type.INTEGER):  objects.Type.BOOLEAN,
            (objects.Type.STRING,  tokens.EQ['name'],       objects.Type.STRING):   objects.Type.BOOLEAN,
            (objects.Type.ARRAY,   tokens.EQ['name'],       objects.Type.ARRAY):    objects.Type.BOOLEAN,
            (objects.Type.INTEGER, tokens.NOT_EQ['name'],   objects.Type.INTEGER):  objects.Type.BOOLEAN,
            (objects.Type.STRING,  tokens.NOT_EQ['name'],   objects.Type.STRING):   objects.Type.BOOLEAN,
            (objects.Type.ARRAY,   tokens.NOT_EQ['name'],   objects.Type.ARRAY):    objects.Type.BOOLEAN,
            (objects.Type.INTEGER, tokens.LESS['name'],     objects.Type.INTEGER):  objects.Type.BOOLEAN,
            (objects.Type.STRING,  tokens.LESS['name'],     objects.Type.STRING):   objects.Type.BOOLEAN,
            (objects.Type.ARRAY,   tokens.LESS['name'],     objects.Type.ARRAY):    objects.Type.BOOLEAN,
            (objects.Type.INTEGER, tokens.GREATER['name'],  objects.Type.INTEGER):  objects.Type.BOOLEAN,
            (objects.Type.STRING,  tokens.GREATER['name'],  objects.Type.STRING):   objects.Type.BOOLEAN,
            (objects.Type.ARRAY,   tokens.GREATER['name'],  objects.Type.ARRAY):    objects.Type.BOOLEAN,
        }

    def new_object(self, typename, value):
        if typename == objects.Type.ARRAY:
            return objects.Array(value)
        elif typename == objects.Type.STRING:
            return objects.String(value)
        elif typename == objects.Type.INTEGER:
            return objects.Number(value)
        elif typename == objects.Type.BOOLEAN:
            return objects.Boolean(value)

    def to_boolean(self, obj):
        if obj.type( ) == objects.Type.BOOLEAN:
            return obj.value( )
        elif obj.type( ) == objects.Type.INTEGER:
            return obj.value( ) != 0
        raise ExecutionError( 'Unable to convert to BOOLEAN: \'{0}\''.format(obj.type( )) )

    def to_integer(self, obj):
        if obj.type( ) == objects.Type.BOOLEAN:
            return 1 if obj.value( ) else 0
        elif obj.type( ) == objects.Type.INTEGER:
            return obj.value( )
        raise ExecutionError( 'Unable to convert to INTEGER: \'{0}\''.format(obj.type( )) )

    def eval_number(self, node, env):
        return objects.Number(node.value( ))

    def eval_boolean(self, node, env):
        return objects.Boolean(node.value( ))

    def eval_string(self, node, env):
        return objects.String(node.value( ))

    def eval_array(self, node, env):
        expr = []
        for a in node.value( ):
            expr.append(self.eval_next(a, env))
        return objects.Array(expr)

    def eval_fn(self, node, env):
        return objects.Function(node.idents, astree.Scope(node.body), env)

    def eval_call(self, node, env):
        expr = self.eval_next(node.value( ),  env)
        if isinstance(expr,  objects.Function):
            if len(node.params( )) < len(expr.params( )):
                raise ExecutionError("Not enough actual parameters for function" )
            call_env = expr.env( ).create_child( )
            call_par = 0
            for id in node.params( ):
                next_res = self.eval_next( id, env )
                call_env.set( expr.params( )[call_par].value( ), next_res )
                call_par += 1
            return self.eval_next(expr.body( ), call_env )
        else:
            raise ExecutionError("'{0}' is tot a callable object".format(expr.type( ) ) )

    def eval_prefix(self, node, env):
        expr = self.eval_next(node.value( ), env)
        cort = (node.operator( ), expr.type( ))
        if cort in self.oper_prefix:
            obj_type = self.oper_prefix[cort]
            if node.operator( ) == '!':
                return self.new_object(obj_type, not self.to_boolean(expr))
            elif node.operator( ) == '-':
                return self.new_object(obj_type, -1 * self.to_integer(expr))
            else:
                raise ExecutionError("Invalid prefix operation '{0}' for '{1}'".
                    format(node.operator( ), expr.type( ) ) )
        else:
            raise ExecutionError("Prefix operation '{0}' is not defined for '{1}'".
                format(node.operator( ), expr.type( ) ) )

    def eval_infix(self, node, env):
        left = self.eval_next(node.left( ), env)
        right = self.eval_next(node.right( ), env)
        cort = (left.type( ), node.operator( ), right.type( ))
        if cort in self.oper_infix:
            obj_type = self.oper_infix[cort]
            if node.operator( ) == '+':
                return self.new_object(obj_type, left.value( ) + right.value( ))
            elif node.operator( ) == '-':
                return self.new_object(obj_type, left.value( ) - right.value( ))
            elif node.operator( ) == '*':
                return self.new_object(obj_type, left.value( ) * right.value( ))
            elif node.operator( ) == '/':
                return self.new_object(obj_type, left.value( ) / right.value( ))
            elif node.operator( ) == '==':
                return self.new_object(obj_type, left.value( ) == right.value( ))
            elif node.operator( ) == '!=':
                return self.new_object(obj_type, left.value( ) != right.value( ))
            elif node.operator( ) == '<':
                return self.new_object(obj_type, left.value( ) < right.value( ))
            elif node.operator( ) == '>':
                return self.new_object(obj_type, left.value( ) > right.value( ))
            else:
                raise ExecutionError("Invalid infix operation '{0}' for '{1}' and '{2}'".
                    format(node.operator( ), left.type( ), right.type( ) ) )
        else:
            raise ExecutionError("Infix operation '{0}' is not defined for '{1}' and '{2}'".
                format(node.operator( ), left.type( ), right.type( ) ) )

    def eval_let(self, node, env):
        env.set(node.ident, self.eval_next(node.expr, env))

    def eval_ident(self, node, env):
        res = env.get(node.value( ))
        if not res:
            raise ExecutionError('Undefined identifier {0}'.format(node.value( )))
        return res

    def eval_return(self, node, env):
        return objects.Return(self.eval_next(node.value( )))

    def eval_scope(self, node, env):
        res = None
        for next in node.value( ):
            res = self.eval_next(next,  env)
            if isinstance(node, objects.Return):
                break
        return res

    def eval_next(self, node,  env):
        res = None
        if isinstance(node, astree.Scope):
            res = self.eval_scope(node, env)

        elif isinstance(node, astree.Let):
            res = self.eval_let(node, env)

        elif isinstance(node, astree.Number):
            res = self.eval_number(node, env)

        elif isinstance(node, astree.Boolean):
            res = self.eval_boolean(node, env)

        elif isinstance(node, astree.String):
            res = self.eval_string(node, env)

        elif isinstance(node, astree.Ident):
            res = self.eval_ident(node, env)

        elif isinstance(node, astree.Array):
            res = self.eval_array(node, env)

        elif isinstance(node, astree.Prefix):
            res = self.eval_prefix(node, env)

        elif isinstance(node, astree.Infix):
            res = self.eval_infix(node, env)

        elif isinstance(node, astree.Function):
            res = self.eval_fn(node, env)

        elif isinstance(node, astree.Call):
            res = self.eval_call(node, env)
        return res

    def eval(self):
        res = self.eval_next(self.ast, self.env)
        return res if not isinstance(res, objects.Return) else res.value( )
