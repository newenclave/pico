from . import lexer
from . import tokens
from . import ast

class ParserError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return 'parser error: ' + repr(self.value)

class Parser(object):

    class precedence:
        LOWEST          = 0
        INFIF           = 1 # infix if
        EQUALS          = 2 # == or !=
        LESSGREATER     = 3 # > or <
        SUM             = 4 # + or -
        PRODUCT         = 5 # * or /
        PREFIX          = 6 # -X or !X
        CALL            = 7 # myFunction(X)
        INDEX           = 8 # array[index]

    def __init__(self,  input):
        lex = lexer.Lexer( )
        self.tokens = lex.get(input)
        self.tokens.append(lexer.Token(tokens.EOF, 'EOF'))
        self.current_id = 0
        self.peek_id = 1 if len(self.tokens) > 1 else 0

        self.nuds = {
            tokens.LPAREN:   self.get_paren,
            tokens.IDENT:    self.get_ident,
            tokens.NUMBER:   self.get_number,
            tokens.STRING:   self.get_string,
            tokens.TRUE:     self.get_bool,
            tokens.FALSE:    self.get_bool,
            tokens.BANG:     self.get_prefix,
            tokens.MINUS:    self.get_prefix,
            tokens.FN:       self.get_fn,
            tokens.IF:       self.get_if,
            tokens.LBRACKET: self.get_array,
            tokens.LBRACE:   self.get_table,

        }
        self.leds = {
            tokens.PLUS:        self.get_infix,
            tokens.MINUS:       self.get_infix,
            tokens.ASTERISK:    self.get_infix,
            tokens.SLASH:       self.get_infix,
            tokens.EQ:          self.get_infix,
            tokens.NOT_EQ:      self.get_infix,
            tokens.LESS:        self.get_infix,
            tokens.GREATER:     self.get_infix,
            tokens.LESS_EQ:     self.get_infix,
            tokens.GREATER_EQ:  self.get_infix,

            tokens.LBRACKET:    self.get_index,
            tokens.LPAREN:      self.get_call,
            tokens.IF:          self.get_infif,
        }

    def precedence_for(self, token):
        vals = {
            tokens.IF:          self.precedence.INFIF,
            tokens.EQ:          self.precedence.EQUALS,
            tokens.NOT_EQ:      self.precedence.EQUALS,
            tokens.LESS:        self.precedence.LESSGREATER,
            tokens.GREATER:     self.precedence.LESSGREATER,
            tokens.LESS_EQ:     self.precedence.LESSGREATER,
            tokens.GREATER_EQ:  self.precedence.LESSGREATER,
            tokens.MINUS:       self.precedence.SUM,
            tokens.PLUS:        self.precedence.SUM,
            tokens.ASTERISK:    self.precedence.PRODUCT,
            tokens.SLASH:       self.precedence.PRODUCT,
            tokens.LPAREN:      self.precedence.CALL,
            tokens.LBRACKET:    self.precedence.INDEX,
        }

        if token in vals:
            return vals[token]
        else:
            return self.precedence.LOWEST

    def token_nud(self,  token):
        if token in self.nuds:
            return self.nuds[token]
        else:
            return None

    def token_led(self,  token):
        if token in self.leds:
            return self.leds[token]
        else:
            return None

    def advance(self):
        self.current_id = self.peek_id
        if not self.eof( ):
            self.peek_id = self.peek_id + 1

    def current(self):
        return self.tokens[self.current_id]

    def current_inf(self):
        return self.current( ).value( )

    def current_lit(self):
        return self.current( ).literal( )

    def peek(self):
        return self.tokens[self.peek_id]

    def peek_inf(self):
        return self.peek( ).value( )

    def peek_precedence(self):
        return self.precedence_for(self.peek_inf( ))

    def eof(self):
        return self.is_current(tokens.EOF)

    def is_current(self, token):
        return self.current_inf( ) == token

    def is_peek(self, token):
        return self.peek_inf( ) == token

    def is_expected( self, token, is_error = True ):
        if self.is_peek(token):
            self.advance( )
            return True
        elif is_error:
            raise ParserError('Unexpecteded token "' + \
                  self.peek_inf( ).name( ) + '". ' + \
                  'expecteded token to be "' + token.name( ) + '"')

        return False

    def get_ident( self ):
        return ast.Ident(self.current_lit( ))

    def get_number( self ):
        return ast.Number( int(self.current_lit( )) )

    def get_string( self ):
        res = ast.String(self.current_lit( ))
        while self.is_expected(tokens.STRING, is_error = False):
            res.val += self.current_lit( )
        return res

    def get_bool( self ):
        return ast.Boolean(self.is_current(tokens.TRUE))

    def get_prefix( self ):
        oper = self.current_inf( )
        self.advance( )
        expr = self.get_expression( prec = self.precedence.PREFIX )
        return ast.Prefix(oper,  expr)

    def get_infix( self, left ):
        oper = self.current_inf( )
        current_precedence = self.precedence_for(self.current_inf( ))
        self.advance( )
        right = self.get_expression( prec = current_precedence )
        return ast.Infix(oper, left, right)


    def get_paren(self):
        self.advance( )
        res = self.get_expression( )
        self.is_expected(tokens.RPAREN)
        return res

    def get_expression(self, prec = precedence.LOWEST ):
        nud = self.token_nud(self.current_inf( ))
        if not nud:
            raise ParserError( 'prefix function '
                               'for {0} is not defined'.
                               format(self.current_inf( )) )
        left = nud( )
        pp = self.peek_precedence( )
        while (not self.is_peek(tokens.SEMICOLON)) and (prec < pp):
            ptok = self.peek_inf( )
            led = self.token_led(ptok)
            if not led:
                raise ParserError( 'infix function '
                                   'for {0} is not defined'.
                                    format(self.peek_inf( )) )
            self.advance( )
            left = led(left)
            pp = self.peek_precedence( )
        return left

    def get_fn(self):
        self.is_expected(tokens.LPAREN) # fn -> (
        self.advance( )                 # ( -> ...
        idents = []

        while self.is_current(tokens.IDENT):
            idents.append(self.get_ident())
            if not self.is_expected(tokens.COMMA, is_error = False):
                break
            self.advance( )

        if not self.is_current(tokens.RPAREN):
            self.is_expected(tokens.RPAREN) # .. -> )

        self.is_expected(tokens.LBRACE) # ) -> {
        self.advance( )                 # { -> ..
        body = self.get_scope(tokens.RBRACE)
        return ast.Function(idents, ast.Scope(body))

    def get_if(self):
        self.is_expected(tokens.LPAREN) # if -> (
        self.advance( )                 # ( -> ...
        cond = self.get_expression( )

        self.is_expected(tokens.RPAREN)
        self.is_expected(tokens.LBRACE)
        self.advance( )

        body = self.get_scope(tokens.RBRACE)
        altbody = []
        if self.is_expected(tokens.ELSE, is_error = False):
            self.is_expected(tokens.LBRACE)
            self.advance( )
            altbody = self.get_scope(tokens.RBRACE)
        return ast.IfElse(cond, ast.Scope(body), ast.Scope(altbody))


    def get_infif(self, left):
        self.advance( )
        cond = self.get_expression( )
        altbody = []
        if self.is_expected(tokens.ELSE, is_error = False):
            self.advance( )
            altbody = [self.get_expression( )]
        return ast.IfElse(cond,  ast.Scope([left]),  ast.Scope(altbody))

    def get_array(self):
        self.advance( )
        expr = []
        if self.is_current(tokens.RBRACKET):
            ast.Array(expr)
        while not self.is_current(tokens.RBRACKET):
            expr.append(self.get_expression( ))
            if not self.is_expected(tokens.COMMA, is_error = False):
                break
            self.advance( )
        self.is_expected(tokens.RBRACKET)
        return ast.Array(expr)

    def get_table(self):
        self.advance( )
        expr = [ ]
        if self.is_current(tokens.RBRACE):
            return ast.Table(expr)

        while not self.is_current(tokens.RBRACE):
            key = self.get_expression( )
            self.is_expected(tokens.COLON)
            self.advance( )
            val = self.get_expression( )
            expr.append((key,  val))
            if not self.is_expected(tokens.COMMA, is_error = False):
                break
            self.advance( )
        self.is_expected(tokens.RBRACE)
        return ast.Table(expr)

    def get_index(self,  obj):
        self.advance( )
        expr = self.get_expression( )
        self.is_expected(tokens.RBRACKET)
        return ast.Index(obj,  expr)

    def get_call(self,  obj):
        expr = []
        self.advance( )
        if self.is_current(tokens.RPAREN):
            return ast.Call(obj, expr)

        while not self.is_current(tokens.RPAREN):
            expr.append(self.get_expression( ))
            if not self.is_expected(tokens.COMMA, is_error = False):
                break
            self.advance( )

        self.is_expected(tokens.RPAREN)
        return ast.Call(obj, expr)

    def get_return(self):
        self.advance( )
        expr = self.get_expression( )
        return ast.Return(expr)

    def get_let(self):
        self.is_expected(tokens.IDENT)
        name = self.current_lit( )
        self.is_expected(tokens.ASSIGN)
        self.advance( )
        expr = self.get_expression( )
        return ast.Let(name,  expr)

    def get_scope(self, stop_token):
        stmts = [ ]
        while not self.is_current(stop_token):
            stmt = None
            if self.is_current(tokens.LET):
                stmt = self.get_let( )
            elif self.is_current(tokens.RETURN):
                stmt = self.get_return( )
            elif self.is_current(tokens.SEMICOLON):
                pass
            else:
                stmt = self.get_expression( )
            if stmt:
                stmts.append(stmt)
            self.advance( )
        return stmts

    def get(self):
        return ast.Scope(self.get_scope(tokens.EOF))

