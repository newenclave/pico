import lexer
import tokens

class parser(object):

    def __init__(self,  input):
        lex = lexer.lexer( )

        self.nuds = { }
        self.leds = { }

        self.tokens = lex.get(input)
        self.tokens.append((tokens.EOF,  'EOF'))
        self.current_id = 0
        self.peek_id    = 1 if len(self.tokens) else 0

    def advance(self):
        self.current_id = self.peek_id
        if not self.eof( ):
            self.peek_id = self.peek_id + 1

    def current(self):
        return self.tokens[self.current_id]

    def peek(self):
        return self.tokens[self.peek_id]

    def eof(self):
        return self.current( )[0] == tokens.EOF

