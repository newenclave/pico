import tokens

class Lexer(object):

    def __init__(self):
        self.tknz = tokens.Tokenizer( )
        self.tknz.set('fn',         tokens.FN)
        self.tknz.set('return',     tokens.RETURN)
        self.tknz.set('let',        tokens.LET)
        self.tknz.set('if',         tokens.IF)
        self.tknz.set('else',       tokens.ELSE)
        self.tknz.set('false',      tokens.FALSE)
        self.tknz.set('true',       tokens.TRUE)

        self.tknz.set('=',          tokens.ASSIGN)
        self.tknz.set('<',          tokens.LESS)
        self.tknz.set('>',          tokens.GREATER)
        self.tknz.set('==',         tokens.EQ)
        self.tknz.set('!=',         tokens.NOT_EQ)
        self.tknz.set('+',          tokens.PLUS)
        self.tknz.set('-',          tokens.MINUS)
        self.tknz.set('*',          tokens.ASTERISK)
        self.tknz.set('/',          tokens.SLASH)
        self.tknz.set('!',          tokens.BANG)
        self.tknz.set(',',          tokens.COMMA)
        self.tknz.set(';',          tokens.SEMICOLON)

        self.tknz.set('(',          tokens.LPAREN)
        self.tknz.set(')',          tokens.RPAREN)

        self.tknz.set('{',          tokens.LBRACE)
        self.tknz.set('}',          tokens.RBRACE)

        self.tknz.set('[',          tokens.LBRACKET)
        self.tknz.set(']',          tokens.RBRACKET)

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
                res = res + escape[input[1]]
                input = input[2:]
            elif input[0] == '"':
                return (res,  input[1:])
            else:
                res = res + input[0]
                input = input[1:]
        return (res,  input)

    def get( self, input ):
        result = [ ]
        while len(input):
            next = self.tknz.get(input)
            if next:
                tmp   = input[next[1]:]
                ident = (len(tmp) > 0) and (self.isident(tmp[0]))
                if next[0][1] and ident:
                    val = self.read_ident(input)
                    result.append( (tokens.IDENT,  val[0]) )
                    input = val[1]
                else:
                    result.append( (next[0],  input[0:next[1]]) )
                    input = tmp
            elif self.isnumeric(input[0]):
                val = self.read_number(input)
                result.append( (tokens.NUMBER,  val[0]) )
                input = val[1]
            elif self.isident(input[0]):
                val = self.read_ident(input)
                result.append( (tokens.IDENT,  val[0]) )
                input = val[1]
            elif input[0] == '"':
                val = self.read_string(input[1:])
                result.append( (tokens.STRING,  val[0]) )
                input = val[1]
            else:
                input = input[1:]
        return result