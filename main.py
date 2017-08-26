
import parser
from syntax_tree import *

#test = 'let a = fn(x, y) { return x + y }'
test = '''
    let a = 100
    let b = 200
    let c = a + b * a
    return -3 * 4 + 2 * 2 - 3 * 5 + 7 / 3
'''

if __name__ == '__main__':
    parse = parser.Parser(test)
    res = parse.get( )
    for i in res:
        print(i)

