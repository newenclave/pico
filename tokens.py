
LET         = {'name': 'let',       'ident': True}
RETURN      = {'name': 'return',    'ident': True}
FN          = {'name': 'fn',        'ident': True}
IF          = {'name': 'if',        'ident': True}
ELSE        = {'name': 'else',      'ident': True}
FALSE       = {'name': 'false',     'ident': True}
TRUE        = {'name': 'true',      'ident': True}

ASSIGN      = {'name': '=',         'ident': False}
EQ          = {'name': '==',        'ident': False}
NOT_EQ      = {'name': '!=',        'ident': False}
LESS        = {'name': '<',         'ident': False}
GREATER     = {'name': '>',         'ident': False}
PLUS        = {'name': '+',         'ident': False}
MINUS       = {'name': '-',         'ident': False}
ASTERISK    = {'name': '*',         'ident': False}
SLASH       = {'name': '/',         'ident': False}
BANG        = {'name': '!',         'ident': False}
COMMA       = {'name': ',',         'ident': False}
COLON       = {'name': ':',         'ident': False}
SEMICOLON   = {'name': ';',         'ident': False}
LPAREN      = {'name': '(',         'ident': False}
RPAREN      = {'name': ')',         'ident': False}
LBRACE      = {'name': '{',         'ident': False}
RBRACE      = {'name': '}',         'ident': False}
LBRACKET    = {'name': '[',         'ident': False}
RBRACKET    = {'name': ']',         'ident': False}

STRING      = {'name': 'STRING',    'ident': False}
NUMBER      = {'name': 'NUMBER',    'ident': False}
IDENT       = {'name': 'IDENT',     'ident': False}
EOF         = {'name': 'EOF',       'ident': False}

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
        return (result['value'],  size) if result else None
