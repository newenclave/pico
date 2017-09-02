
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
    t.set('a',  0)
    t.set('cat',  1)
    t.set('ca',   1.5)
    t.set('dog',  2)
    t.set('fox',  3)
    t.set('fire', 4)
    print(t.values)

    #REPL( )
    e = env.Environment( )
    e.set('len',   builtin.Len(e))
    e.set('print', builtin.Print(e))
    e.set('input', builtin.Input(e))
    res = parser.Parser(test).get( )
    wlk = walker.Walker(res, e)
    print(wlk.eval( ))


