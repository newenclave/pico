
LET         = 'LET'
RETURN      = 'RETURN'
FN          = 'FN'
IF          = 'IF'
ELSE        = 'ELSE'
FALSE       = 'FALSE'
TRUE        = 'TRUE'
END         = 'END'

ASSIGN      = 'ASSIGN'
EQ          = 'EQ'
NOT_EQ      = 'NOT_EQ'
LESS        = 'LESS'
GREATER     = 'GREATER'
LESS_EQ     = 'LESS_EQ'
GREATER_EQ  = 'GREATER_EQ'
PLUS        = 'PLUS'
MINUS       = 'MINUS'
ASTERISK    = 'ASTERISK'
SLASH       = 'SLASH'
BANG        = 'BANG'
COMMA       = 'COMMA'
COLON       = 'COLON'
SEMICOLON   = 'SEMICOLON'
LPAREN      = 'LPAREN'
RPAREN      = 'RPAREN'
LBRACE      = 'LBRACE'
RBRACE      = 'RBRACE'
LBRACKET    = 'LBRACKET'
RBRACKET    = 'RBRACKET'

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
        return (result['value'], size) if result else (None,  0)
