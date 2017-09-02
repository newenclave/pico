
import parser
import environment as env
import walker
import builtin
import tokens

test = '''
let fib = fn( n ) {
    let impl = fn( a, b, n ) {
        if(n > 0) {
            impl( b, a + b, n -1 )
        } else {
            a
        }
    }
    impl(0, 1, n)
}
print(fib(100))
'''

def REPL( ):
    e = env.Environment( )
    e.set('len',   builtin.Len(e))
    e.set('print', builtin.Print(e))
    e.set('input', builtin.Input(e))
    while True:
        try:
            str = input('>>> ')
            if str == 'exit':
                break
            parse = parser.Parser(str)
            res = parse.get( )
            wlk = walker.Walker(res, e)
            res = wlk.eval( )
            if res:
                print(res)
        except Exception as ex:
            print("Exception: ",  ex)

if __name__ == '__main__':
    t = tokens.Tokenizer( )
    t.set('if',     'IF')
    t.set('else',   'ELSE')
    t.set('let',    'LET')
    t.set('return', 'RETURN')
    t.set(' ',      'SPACE')
    t.set('=',      'ASSIGN')
    t.set('==',     'EQUAL')
    t.set('===',    'DEEPEQUAL')

    string = 'if else let return === = =='
    while len(string):
        next = t.get(string)
        print(next[0])
        string = string[next[1]:]
    exit(1)
    REPL( )
    e = env.Environment( )
    e.set('len',   builtin.Len(e))
    e.set('print', builtin.Print(e))
    e.set('input', builtin.Input(e))
    res = parser.Parser(test).get( )
    wlk = walker.Walker(res, e)
    print(wlk.eval( ))


