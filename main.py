
import parser
from syntax_tree import *

#test = 'let a = fn(x, y) { return x + y }'
test = '''
    return -2 + 2 * 2
'''

if __name__ == '__main__':
    parse = parser.Parser(test)
    res = parse.get( )
    for i in res:
        print(i)

