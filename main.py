
import pico.parser
import pico.environment as env
import pico.walker
import pico.builtin
import pico.lexer
import pico.tokens

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
    e.set('len',   pico.builtin.Len(e))
    e.set('print', pico.builtin.Print(e))
    e.set('input', pico.builtin.Input(e))
    while True:
        try:
            str = input('>>> ')
            if str == 'exit':
                break
            parse = pico.parser.Parser(str)
            res = parse.get( )
            wlk = pico.walker.Walker(res, e)
            res = wlk.eval( )
            if res:
                print(res)
        except Exception as ex:
            print("Exception: ",  ex)

if __name__ == '__main__':
    lex = pico.lexer.Lexer( )
    input = 'let a = 10; '      \
            'let b = "hello!"'  \
            'let c = "less" if a < 10 else "greater"'
    res = lex.get(input)
    for r in res:
        print(r,  end=", ")
    print( )
    #exit(1)
    #REPL( )
    e = env.Environment( )
    e.set('len',   pico.builtin.Len(e))
    e.set('print', pico.builtin.Print(e))
    e.set('input', pico.builtin.Input(e))
    res = pico.parser.Parser(test).get( )
    wlk = pico.walker.Walker(res, e)
    print(wlk.eval( ))


