import lexer
import tokens

from syntax_tree import *

class ParserError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return 'parser error: ' + repr(self.value)

class Parser(object):

    class precedence:
        LOWEST          = 0
        EQUALS          = 1, # ==
        LESSGREATER     = 2, # > or <
        SUM             = 3, # +
        PRODUCT         = 4, # *
        PREFIX          = 5, # -X or !X
        CALL            = 6, # myFunction(X)
        INDEX           = 7, # array[index]

    def __init__(self,  input):
        lex = lexer.Lexer( )
        self.tokens = lex.get(input)
        self.tokens.append((tokens.EOF,  'EOF'))
        self.current_id = 0
        self.peek_id = 1 if len(self.tokens) > 1 else 0

        self.nuds = {
            tokens.IDENT:  self.get_ident,
            tokens.NUMBER: self.get_number,
            tokens.STRING: self.get_string,
            tokens.TRUE:   self.get_bool,
            tokens.FALSE:  self.get_bool,
            tokens.BANG:   self.get_prefix,
            tokens.MINUS:  self.get_prefix,
        }
        self.leds = { }

    def advance(self):
        self.current_id = self.peek_id
        if not self.eof( ):
            self.peek_id = self.peek_id + 1

    def current(self):
        return self.tokens[self.current_id]

    def current_tok(self):
        return self.current( )[0]

    def current_lex(self):
        return self.current( )[1]

    def peek(self):
        return self.tokens[self.peek_id]

    def eof(self):
        return self.is_current(tokens.EOF)

    def is_current(self, token):
        return self.current( )[0] == token

    def is_peek(self, token):
        return self.peek( )[0] == token

    def expect( self, token,  is_error = True ):
        if self.is_peek(token):
            self.advance( )
            return True
        elif is_error:
            raise ParserError('Unexpected token "' + \
                  self.peek( )[0] + '". ' + \
                  'Expected token to be "' + token[0] + '"')

        return False

    def get_ident( self ):
        return expressions.Ident(self.current_lex( ))

    def get_number( self ):
        return expressions.Number(self.current_lex( ))

    def get_string( self ):
        return expressions.String(self.current_lex( ))

    def get_bool( self ):
        return expressions.Bool(self.is_current(tokens.TRUE))

    def get_prefix( self ):
        oper = self.current_lex( )
        self.advance( )
        expr = self.get_expression( prec = self.precedence.PREFIX )
        return expressions.Prefix(oper,  expr)

    def get_expression(self, prec = precedence.LOWEST ):
        if not self.current_tok( ) in self.nuds:
            raise ParserError( 'prefix function '
                               'for {0} is not defined'.
                               format(self.current_tok( )) )
        nud = self.nuds[self.current_tok( )]
        left = nud( )
        return left

    def get_return(self):
        self.advance( )
        expr = self.get_expression( )
        return statements.Return(expr)

    def get_let(self):
        self.expect(tokens.IDENT)
        name = self.current( )[1]
        self.expect(tokens.ASSIGN)
        self.advance( )
        expr = self.get_expression( )
        return statements.Let(name,  expr)

    def get(self):
        stmts = [ ]
        while not self.eof( ):
            stmt = None
            if self.is_current(tokens.LET):
                stmt = self.get_let( )
            elif self.is_current(tokens.RETURN):
                stmt = self.get_return( )
            else:
                stmt = self.get_expression( )

            if stmt:
                stmts.append(stmt)
            self.advance( )
        return stmts

