
import parser
import environment as env
import walker
import builtin

test = '''
    if(1<1) { } else { }
    let a = 100
'''

def REPL():
    e = env.Environment( )
    e.set('len',  builtin.Len(e))
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

