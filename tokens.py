
LET         = 'let'
RETURN      = 'return'
FN          = 'fn'
IF          = 'if'
ELSE        = 'else'
FALSE       = 'false'
TRUE        = 'true'

ASSIGN      = '='
EQ          = '=='
NOT_EQ      = '!='
LESS        = '<'
GREATER     = '>'
LESS_EQ     = '<='
GREATER_EQ  = '>='
PLUS        = '+'
MINUS       = '-'
ASTERISK    = '*'
SLASH       = '/'
BANG        = '!'
COMMA       = ','
COLON       = ':'
SEMICOLON   = ';'
LPAREN      = '('
RPAREN      = ')'
LBRACE      = '{'
RBRACE      = '}'
LBRACKET    = '['
RBRACKET    = ']'

STRING      = 'STRING'
NUMBER      = 'NUMBER'
IDENT       = 'IDENT'
EOF         = 'EOF'

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
