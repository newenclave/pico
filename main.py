
import parser
import environment as env
import walker
import builtin

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
fib(140)
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
    REPL( )
    #e = env.Environment( )
    #res = parser.Parser(test).get( )
    #wlk = walker.Walker(res, e)
    #print(wlk.eval( ))


