
import parser
from syntax_tree import *

#test = 'let a = fn(x, y) { return x + y }'
test = '''
    let a = fn(a, b ) { a + b }
    let b = 200
    let c = a + b * a;
    return -3 * 4 + 2 * 2 - 3 * 5 + 7 / 3
    if(a < 100) { a + 100 }
'''

if __name__ == '__main__':
    
    try:
        parse = parser.Parser(test)
        #print(parse.tokens)
        res = parse.get( )
        for i in res:
            print(i)
    except Exception as e:
        print('Exception: ', e)
    
