import lexer
import tokens
import astree

class ParserError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return 'parser error: ' + repr(self.value)

class Parser(object):

    class precedence:
        LOWEST          = 0
        EQUALS          = 1 # == or !=
        LESSGREATER     = 2 # > or <
        SUM             = 3 # + or -
        PRODUCT         = 4 # * or /
        PREFIX          = 5 # -X or !X
        CALL            = 6 # myFunction(X)
        INDEX           = 7 # array[index]

    def __init__(self,  input):
        lex = lexer.Lexer( )
        self.tokens = lex.get(input)
        self.tokens.append({ 'token': tokens.EOF, 'literal': 'EOF'})
        self.current_id = 0
        self.peek_id = 1 if len(self.tokens) > 1 else 0

        self.nuds = {
            tokens.LPAREN['name']:   self.get_paren,
            tokens.IDENT['name']:    self.get_ident,
            tokens.NUMBER['name']:   self.get_number,
            tokens.STRING['name']:   self.get_string,
            tokens.TRUE['name']:     self.get_bool,
            tokens.FALSE['name']:    self.get_bool,
            tokens.BANG['name']:     self.get_prefix,
            tokens.MINUS['name']:    self.get_prefix,
            tokens.FN['name']:       self.get_fn,
            tokens.IF['name']:       self.get_if,
            tokens.LBRACKET['name']: self.get_array,
            tokens.LBRACE['name']:   self.get_table,

        }
        self.leds = {
            tokens.PLUS['name']:        self.get_infix,
            tokens.MINUS['name']:       self.get_infix,
            tokens.ASTERISK['name']:    self.get_infix,
            tokens.SLASH['name']:       self.get_infix,
            tokens.EQ['name']:          self.get_infix,
            tokens.NOT_EQ['name']:      self.get_infix,
            tokens.LESS['name']:        self.get_infix,
            tokens.GREATER['name']:     self.get_infix,
            tokens.LESS_EQ['name']:     self.get_infix,
            tokens.GREATER_EQ['name']:  self.get_infix,

            tokens.LBRACKET['name']:    self.get_index,
            tokens.LPAREN['name']:      self.get_call,
        }

    def precedence_for(self, token):
        vals = {
            tokens.EQ['name']:          self.precedence.EQUALS,
            tokens.NOT_EQ['name']:      self.precedence.EQUALS,
            tokens.LESS['name']:        self.precedence.LESSGREATER,
            tokens.GREATER['name']:     self.precedence.LESSGREATER,
            tokens.LESS_EQ['name']:     self.precedence.LESSGREATER,
            tokens.GREATER_EQ['name']:  self.precedence.LESSGREATER,
            tokens.MINUS['name']:       self.precedence.SUM,
            tokens.PLUS['name']:        self.precedence.SUM,
            tokens.ASTERISK['name']:    self.precedence.PRODUCT,
            tokens.SLASH['name']:       self.precedence.PRODUCT,
            tokens.LPAREN['name']:      self.precedence.CALL,
            tokens.LBRACKET['name']:    self.precedence.INDEX,
        }

        if token['name'] in vals:
            return vals[token['name']]
        else:
            return self.precedence.LOWEST

    def token_nud(self,  token):
        if token['name'] in self.nuds:
            return self.nuds[token['name']]
        else:
            return None

    def token_led(self,  token):
        if token['name'] in self.leds:
            return self.leds[token['name']]
        else:
            return None

    def advance(self):
        self.current_id = self.peek_id
        if not self.eof( ):
            self.peek_id = self.peek_id + 1

    def current(self):
        return self.tokens[self.current_id]

    def current_tok(self):
        return self.current( )['token']

    def current_lit(self):
        return self.current( )['literal']

    def peek(self):
        return self.tokens[self.peek_id]

    def peek_tok(self):
        return self.peek( )['token']

    def peek_precedence(self):
        return self.precedence_for(self.peek_tok( ))

    def eof(self):
        return self.is_current(tokens.EOF)

    def is_current(self, token):
        return self.current( )['token'] == token

    def is_peek(self, token):
        return self.peek( )['token'] == token

    def is_expected( self, token, is_error = True ):
        if self.is_peek(token):
            self.advance( )
            return True
        elif is_error:
            raise ParserError('Unexpecteded token "' + \
                  self.peek_tok( )['name'] + '". ' + \
                  'expecteded token to be "' + token['name'] + '"')

        return False

    def get_ident( self ):
        return astree.Ident(self.current_lit( ))

    def get_number( self ):
        return astree.Number(self.current_lit( ))

    def get_string( self ):
        res = astree.String(self.current_lit( ))
        while self.is_expected(tokens.STRING, is_error = False):
            res.val += self.current_lit( )
        return res

    def get_bool( self ):
        return astree.Boolean(self.is_current(tokens.TRUE))

    def get_prefix( self ):
        oper = self.current_tok( )['name']
        self.advance( )
        expr = self.get_expression( prec = self.precedence.PREFIX )
        return astree.Prefix(oper,  expr)

    def get_infix( self,  left ):
        oper = self.current_lit( )
        current_precedence = self.precedence_for(self.current_tok( ))
        self.advance( )
        right = self.get_expression( prec = current_precedence )
        return astree.Infix(oper, left, right)

    def get_paren(self):
        self.advance( )
        res = self.get_expression( )
        self.is_expected(tokens.RPAREN)
        return res

    def get_expression(self, prec = precedence.LOWEST ):
        nud = self.token_nud(self.current_tok( ))
        if not nud:
            raise ParserError( 'prefix function '
                               'for {0} is not defined'.
                               format(self.current_tok( )) )
        left = nud( )
        pp = self.peek_precedence( )
        while (not self.is_peek(tokens.SEMICOLON)) and (prec < pp):
            ptok = self.peek_tok( )
            led = self.token_led(ptok)
            if not led:
                raise ParserError( 'infix function '
                                   'for {0} is not defined'.
                                    format(self.peek_tok( )) )
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
        return astree.Function(idents, astree.Scope(body))

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
        return astree.IfElse(cond, astree.Scope(body), astree.Scope(altbody))

    def get_array(self):
        self.advance( )
        expr = []
        while not self.is_current(tokens.RBRACKET):
            expr.append(self.get_expression( ))
            if not self.is_expected(tokens.COMMA, is_error = False):
                break
            self.advance( )
        if not self.is_current(tokens.RBRACKET):
            self.is_expected(tokens.RBRACKET)
        return astree.Array(expr)

    def get_table(self):
        self.advance( )
        expr = [ ]
        while not self.is_current(tokens.RBRACE):
            key = self.get_expression( )
            self.is_expected(tokens.COLON)
            self.advance( )
            val = self.get_expression( )
            expr.append((key,  val))
            if not self.is_expected(tokens.COMMA, is_error = False):
                break
            self.advance( )
        if not self.is_current(tokens.RBRACE):
            self.is_expected(tokens.RBRACE)
        return astree.Table(expr)

    def get_index(self,  obj):
        self.advance( )
        expr = self.get_expression( )
        self.is_expected(tokens.RBRACKET)
        return astree.Index(obj,  expr)

    def get_call(self,  obj):
        self.advance( )
        expr = []
        while not self.is_current(tokens.RPAREN):
            expr.append(self.get_expression( ))
            if not self.is_expected(tokens.COMMA, is_error = False):
                break
            self.advance( )
        if not self.is_current(tokens.RPAREN):
            self.is_expected(tokens.RPAREN)
        return astree.Call(obj,  expr)

    def get_return(self):
        self.advance( )
        expr = self.get_expression( )
        return astree.Return(expr)

    def get_let(self):
        self.is_expected(tokens.IDENT)
        name = self.current_lit( )
        self.is_expected(tokens.ASSIGN)
        self.advance( )
        expr = self.get_expression( )
        return astree.Let(name,  expr)

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
        return astree.Scope(self.get_scope(tokens.EOF))

