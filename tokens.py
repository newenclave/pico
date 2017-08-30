
class Value(object):
    def __init__(self, name, ident = False):
        self.name_  = name
        self.ident_ = ident
    def isident(self):
        return self.ident_
    def name(self):
        return self.name_
    def __hash__(self):
        return hash(self.name_)
    def __str__(self):
        return self.name_
    def __eq__(self, other):
        return self.name_ == other.name( )

LET         = Value( 'let',      ident = True )
RETURN      = Value( 'return',   ident = True )
FN          = Value( 'fn',       ident = True )
IF          = Value( 'if',       ident = True )
ELSE        = Value( 'else',     ident = True )
FALSE       = Value( 'false',    ident = True )
TRUE        = Value( 'true',     ident = True )

ASSIGN      = Value( '=',        ident = False )
EQ          = Value( '==',       ident = False )
NOT_EQ      = Value( '!=',       ident = False )
LESS        = Value( '<',        ident = False )
GREATER     = Value( '>',        ident = False )
LESS_EQ     = Value( '<=',       ident = False )
GREATER_EQ  = Value( '>=',       ident = False )
PLUS        = Value( '+',        ident = False )
MINUS       = Value( '-',        ident = False )
ASTERISK    = Value( '*',        ident = False )
SLASH       = Value( '/',        ident = False )
BANG        = Value( '!',        ident = False )
COMMA       = Value( ',',        ident = False )
COLON       = Value( ':',        ident = False )
SEMICOLON   = Value( ';',        ident = False )
LPAREN      = Value( '(',        ident = False )
RPAREN      = Value( ')',        ident = False )
LBRACE      = Value( '{',        ident = False )
RBRACE      = Value( '}',        ident = False )
LBRACKET    = Value( '[',        ident = False )
RBRACKET    = Value( ']',        ident = False )

STRING      = Value( 'STRING',   ident = False )
NUMBER      = Value( 'NUMBER',   ident = False )
IDENT       = Value( 'IDENT',    ident = False )
EOF         = Value( 'EOF',      ident = False )

class Tokenizer(object):

    def __init__(self):
        self.values = { }

    def set( self, key, value ):
        tmp  = self.values
        for i in key:
            if not i in tmp:
                tmp[i] = { }
            tmp = tmp[i]
        tmp['value'] = value
        return tmp

    def get( self, key ):
        tmp    = self.values
        size   = 0
        result = None
        for i in key:
            if not i in tmp: break
            tmp  = tmp[i]
            size = size + 1
            if 'value' in tmp:
                result = tmp
        return (result['value'], size) if result else None
