
import parser
import environment as env
import walker

test = '''
    let a = 1000
    let b = "String"
    let c = fn(){ b + b }
    let d = fn(a, b){ a + b }
    let e = [1, 2, 3, d, b, a]
    let f = e[0]
    let g = d(100, 200)
    return -23452345
'''

def REPL():
    e = env.Environment( )
    while True:
        #try:
            str = input('>>> ')
            if str == 'exit':
                break
            parse = parser.Parser(str)
            res = parse.get( )
            wlk = walker.Walker(res, e)
            print(wlk.eval( ))
        #except Exception as ex:
        #    print("Exception: ",  ex)

if __name__ == '__main__':
    REPL( )

