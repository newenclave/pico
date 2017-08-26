
import parser
from syntax_tree import *

#test = 'let a = fn(x, y) { return x + y }'
test = '''
    let a = 10000
    let b = "Hello, world!"
    let c = !true
    return -1000
'''

if __name__ == '__main__':
    parse = parser.Parser(test)
    res = parse.get( )
    for i in res:
        print(i)

