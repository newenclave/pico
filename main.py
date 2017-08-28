
import parser
import environment as env
import walker
import builtin

test = '''
    let a = {1: 3423}
'''

def REPL():
    e = env.Environment( )
    e.set('len',   builtin.Len(e))
    e.set('print', builtin.Print(e))
    while True:
        try:
            str = input('>>> ')
            if str == 'exit':
                break
            parse = parser.Parser(str)
            res = parse.get( )
            wlk = walker.Walker(res, e)
            print(wlk.eval( ))
        except Exception as ex:
            print("Exception: ",  ex)

if __name__ == '__main__':
    REPL( )
    #parse = parser.Parser(test)
    #print(parse.get( ))

