import parser

#test = 'let a = fn(x, y) { return x + y }'
test = '''
    let a = fn(x, y) { return x * 10 + y }
    let b = "Hello, world!"
    let c = a(10, 20)
'''

if __name__ == '__main__':
    parse = parser.parser(test)
    for i in parse.tokens:
        print(i)

    print(parse.eof())
