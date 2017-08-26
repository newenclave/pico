
LET         = ('let',       True)
RETURN      = ('return',    True)
FN          = ('fn',        True)
IF          = ('if',        True)
ELSE        = ('else',      True)

EQ          = ('==',        False)
ASSIGN      = ('=',         False)
NOT_EQ      = ('!=',        False)
PLUS        = ('+',         False)
MINUS       = ('-',         False)
ASTERISK    = ('*',         False)
SLASH       = ('/',         False)
BANG        = ('!',         False)
COMMA       = (',',         False)
COLON       = (':',         False)
SEMICOLON   = (';',         False)
LPAREN      = ('(',         False)
RPAREN      = (')',         False)
LBRACE      = ('{',         False)
RBRACE      = ('}',         False)
LBRACKET    = ('[',         False)
RBRACKET    = (']',         False)

STRING      = ('STRING',    False)
NUMBER      = ('NUMBER',    False)
IDENT       = ('IDENT',     False)
EOF         = ('EOF',       False)

class tokenizer(object):

    def __init__(self):
        self.values = { }

    def set( self,  key,  value ):
        tmp  = self.values
        for i in key:
            if not i in tmp:
                tmp[i] = { }
            tmp = tmp[i]
        tmp['value'] = value
        return tmp

    def get(self,  key,  greedy = True): # remove greedy value
        tmp    = self.values
        size   = 0
        result = None
        for i in key:
            if not i in tmp: break
            tmp  = tmp[i]
            size = size + 1
            if 'value' in tmp:
                result = tmp
                if not greedy: break
        return (result['value'],  size) if result else None
