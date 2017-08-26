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
        EQUALS          = 1 # ==
        LESSGREATER     = 2 # > or <
        SUM             = 3 # + or -
        PRODUCT         = 4 # * or /
        PREFIX          = 5 # -X or !X
        CALL            = 6 # myFunction(X)
        INDEX           = 7 # array[index]

    def precedence_for(self, token):
        vals = {
            tokens.EQ:       self.precedence.EQUALS,
            tokens.NOT_EQ:   self.precedence.EQUALS,
            tokens.LESS:     self.precedence.LESSGREATER,
            tokens.GREATER:  self.precedence.LESSGREATER,
            tokens.MINUS:    self.precedence.SUM,
            tokens.PLUS:     self.precedence.SUM,
            tokens.ASTERISK: self.precedence.PRODUCT,
            tokens.SLASH:    self.precedence.PRODUCT,
            tokens.LPAREN:   self.precedence.CALL,
            tokens.LBRACKET: self.precedence.INDEX,
        }

        if token in vals:
            return vals[token]
        else:
            return self.precedence.LOWEST

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
        self.leds = {
            tokens.PLUS:        self.get_infix,
            tokens.MINUS:       self.get_infix,
            tokens.ASTERISK:    self.get_infix,
            tokens.SLASH:       self.get_infix,
        }

    def advance(self):
        self.current_id = self.peek_id
        if not self.eof( ):
            self.peek_id = self.peek_id + 1

    def current(self):
        return self.tokens[self.current_id]

    def current_tok(self):
        return self.current( )[0]

    def current_lit(self):
        return self.current( )[1]

    def peek(self):
        return self.tokens[self.peek_id]

    def peek_tok(self):
        return self.peek( )[0]

    def peek_precedence(self):
        return self.precedence_for(self.peek_tok( ))

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
        return expressions.Ident(self.current_lit( ))

    def get_number( self ):
        return expressions.Number(self.current_lit( ))

    def get_string( self ):
        return expressions.String(self.current_lit( ))

    def get_bool( self ):
        return expressions.Bool(self.is_current(tokens.TRUE))

    def get_prefix( self ):
        oper = self.current_lit( )
        self.advance( )
        expr = self.get_expression( prec = self.precedence.PREFIX )
        return expressions.Prefix(oper,  expr)

    def get_infix( self,  left ):
        oper = self.current_lit( )
        current_precedence = self.precedence_for(self.current_tok( ))
        self.advance( )
        right = self.get_expression( prec = current_precedence )
        return expressions.Infix(oper, left, right)

    def get_expression(self, prec = precedence.LOWEST ):
        if not self.current_tok( ) in self.nuds:
            raise ParserError( 'prefix function '
                               'for {0} is not defined'.
                               format(self.current_tok( )) )
        nud = self.nuds[self.current_tok( )]
        left = nud( )
        pp = self.peek_precedence( )
        while (not self.is_peek(tokens.SEMICOLON)) and (prec < pp):
            ptok = self.peek_tok( )
            if not ptok in self.leds:
                raise ParserError( 'infix function '
                                   'for {0} is not defined'.
                                    format(self.peek_tok( )) )
            led = self.leds[ptok]
            self.advance( )
            left = led(left)
            pp = self.peek_precedence( )
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

