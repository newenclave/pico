
import parser
from syntax_tree import *

#test = 'let a = fn(x, y) { return x + y }'
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

if __name__ == '__main__':
    
    try:
        parse = parser.Parser(test)
        res = parse.get( )
        print(res)
    except Exception as e:
        print('Exception: ', e)
    
