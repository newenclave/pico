import tokens

class LexerError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return 'lexer error: ' + repr(self.value)

class Token(object):
    def __init__(self, value, literal):
        self.value_ = value
        self.literal_ = literal
    def value(self):
        return self.value_
    def literal(self):
        return self.literal_
    def __str__(self):
        return '{0}({1})'.format(str(self.value( )), self.literal_)

class Lexer(object):

    def __init__(self):
        self.tknz = tokens.Tokenizer( )
        self.tknz.set('fn',     (tokens.FN,         True ) )
        self.tknz.set('return', (tokens.RETURN,     True ) )
        self.tknz.set('let',    (tokens.LET,        True ) )
        self.tknz.set('if',     (tokens.IF,         True ) )
        self.tknz.set('else',   (tokens.ELSE,       True ) )
        self.tknz.set('false',  (tokens.FALSE,      True ) )
        self.tknz.set('true',   (tokens.TRUE,       True ) )
        #self.tknz.set('end',    (tokens.END,        True ) )

        self.tknz.set('=',      (tokens.ASSIGN,     False) )
        self.tknz.set('<',      (tokens.LESS,       False) )
        self.tknz.set('>',      (tokens.GREATER,    False) )
        self.tknz.set('<=',     (tokens.LESS_EQ,    False) )
        self.tknz.set('>=',     (tokens.GREATER_EQ, False) )
        self.tknz.set('==',     (tokens.EQ,         False) )
        self.tknz.set('!=',     (tokens.NOT_EQ,     False) )
        self.tknz.set('+',      (tokens.PLUS,       False) )
        self.tknz.set('-',      (tokens.MINUS,      False) )
        self.tknz.set('*',      (tokens.ASTERISK,   False) )
        self.tknz.set('/',      (tokens.SLASH,      False) )
        self.tknz.set('!',      (tokens.BANG,       False) )
        self.tknz.set(',',      (tokens.COMMA,      False) )
        self.tknz.set(':',      (tokens.COLON,      False) )
        self.tknz.set(';',      (tokens.SEMICOLON,  False) )

        self.tknz.set('(',      (tokens.LPAREN,     False) )
        self.tknz.set(')',      (tokens.RPAREN,     False) )

        self.tknz.set('{',      (tokens.LBRACE,     False) )
        self.tknz.set('}',      (tokens.RBRACE,     False) )

        self.tknz.set('[',      (tokens.LBRACKET,   False) )
        self.tknz.set(']',      (tokens.RBRACKET,   False) )

    def isident( self, char ):
        return char.isnumeric( ) or char.isalpha( ) or char == '_'

    def isnumeric( self, char ):
        return char.isnumeric( )

    def ischar( self, char ):
        return char.isalfa( ) or char == '_'

    def read_number(self,  input):
        res = ''
        while len(input) > 0 and input[0].isnumeric( ):
            res = res + input[0]
            input = input[1:]
        return (int(res),  input)

    def read_ident(self,  input):
        res = ''
        while len(input) > 0 and self.isident(input[0]):
            res = res + input[0]
            input = input[1:]
        return (res,  input)

    def read_string(self,  input):
        escape = {
            '\\':  '\\',
            'n' :  '\n',
            't' :  '\t',
            'r' :  '\r',
            '"' :  '\"',
        }
        res = ''
        while len(input) > 0:
            if input[0] == '\\' and (len(input) > 1) and (input[1] in escape):
                res += escape[input[1]]
                input = input[2:]
            elif input[0] == '"':
                return (res,  input[1:])
            else:
                res = res + input[0]
                input = input[1:]
        return (res,  input)

    def skip_whitespaces(self,  input):
        size = 0
        while len(input) > size and input[size].isspace( ):
            size = size + 1
        return input[size:]

    def get( self, input ):
        result = [ ]
        input = self.skip_whitespaces(input)
        while len(input):
            next = self.tknz.get(input)
            if next:
                tmp   = input[next[1]:]
                ident = (len(tmp) > 0) and (self.isident(tmp[0]))
                if next[0][1] and ident:
                    val = self.read_ident(input)
                    result.append( Token( tokens.IDENT,  val[0] ) )
                    input = val[1]
                else:
                    result.append( Token( next[0][0],  input[0:next[1]] ) )
                    input = tmp
            elif self.isnumeric(input[0]):
                val = self.read_number(input)
                result.append( Token(tokens.NUMBER,  val[0]) )
                input = val[1]
            elif self.isident(input[0]):
                val = self.read_ident(input)
                result.append( Token( tokens.IDENT,  val[0]) )
                input = val[1]
            elif input[0] == '"':
                val = self.read_string(input[1:])
                result.append( Token( tokens.STRING,  val[0]) )
                input = val[1]
            else:
                raise LexerError("Unexpecteded symbol '{0}'".format(input[0]) )

            input = self.skip_whitespaces(input)

        return result
