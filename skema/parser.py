##
# LR parser generated by the Syntax tool.
#
# https://www.npmjs.com/package/syntax-cli
#
#     npm install -g syntax-cli
#
#     syntax-cli --help
#
# To regenerate run:
#
#     syntax-cli \
#         --grammar ~/path-to-grammar-file \
#         --mode <parsing-mode> \
#         --output ~/parsermodule.py
##

yytext = ''
yyleng = 0

# Semantic value result.
__ = None

# Location restult.
__loc = None

should_capture_locations = False

EOF = '$'

def on_parse_begin(string):
    pass

def on_parse_end(parsed):
    pass



def _handler1(_1):
    global __, __loc, yytext, yyleng
    __ = _1

def _handler2(_1):
    global __, __loc, yytext, yyleng
    __ = _2

productions = [[-1,1,_handler1],
[0,1,_handler2]]
tokens = {"VAL":"1","$":"2"}
table = [{"0":1,"1":"s2"},{"2":"acc"},{"2":"r1"}]

stack = None

##
# Generic tokenizer used by the parser in the Syntax tool.
#
# https://www.npmjs.com/package/syntax-cli
#
# See `--custom-tokinzer` to skip this generation, and use a custom one.
##

import re as _syntax_tool_re

def _lex_rule1(self):
    global __, __loc, yytext, yyleng
    
    last = len(yytext.strip()) - 3
    yytext = yytext[3:last]
    if yytext and yytext[0] == '\n':
        yytext = yytext[1:]
    if yytext and yytext[-1] == '\n':
        yytext = yytext[:-1]
    return 'ANNOTATION'
    

def _lex_rule2(self):
    global __, __loc, yytext, yyleng
    
    last = len(yytext.strip()) - 1
    yytext = yytext[1:last]
    return 'REGEX'
    

def _lex_rule3(self):
    global __, __loc, yytext, yyleng
    
    last = len(yytext.strip()) - 2
    yytext = yytext[0:last]
    return 'OPTIONAL_KEY'
    

def _lex_rule4(self):
    global __, __loc, yytext, yyleng
    
    last = len(yytext.strip()) - 1
    yytext = yytext[0:last]
    return 'REQUIRED_KEY'
    

def _lex_rule5(self):
    global __, __loc, yytext, yyleng
    return '['

def _lex_rule6(self):
    global __, __loc, yytext, yyleng
    return ']'

def _lex_rule7(self):
    global __, __loc, yytext, yyleng
    return '...'

def _lex_rule8(self):
    global __, __loc, yytext, yyleng
    
    # print('token_start_column', self.token_start_column)
    yytext = yytext.replace('!', '')
    yytext = yytext.strip()
    if self.token_start_column == 0:
        last = len(yytext.strip()) - 1
        yytext = yytext[1:last]
        return 'ANNOTATION'
    else:
        return 'VAL'
    

def _lex_rule9(self):
    global __, __loc, yytext, yyleng
    
    if '#' in yytext:
        pass
    else:
        yytext = yytext[1:]
        yytext = len(yytext)
        return 'SEPARATOR'
    

def _lex_rule10(self):
    global __, __loc, yytext, yyleng
    pass

def _lex_rule11(self):
    global __, __loc, yytext, yyleng
    pass

_lex_rules = [['^"""(?:(?!""").|\n)*"""[ ]*', _lex_rule1],
['^/.*/[ ]*', _lex_rule2],
['^[a-zA-Z0-9_]+\?:[ ]*', _lex_rule3],
['^[a-zA-Z0-9_]+:[ ]*', _lex_rule4],
['^\[[ ]*', _lex_rule5],
['^\][ ]*', _lex_rule6],
['^\.\.\.[ ]*', _lex_rule7],
['^[a-zA-Z0-9_&\| !."]+', _lex_rule8],
['^\n((?:[ ]|#.*)*)', _lex_rule9],
['^#.*', _lex_rule10],
['^\s+', _lex_rule11]]

_lex_rules_by_conditions = {"INITIAL":[0,1,2,3,4,5,6,7,8,9,10]}

EOF_TOKEN = {
  'type': EOF,
  'value': ''
}

class Tokenizer(object):
    _string = None
    _cursor = 0

    # Line-based location tracking.
    _current_line = 1
    _current_column = 0
    _current_line_begin_offset = 0

    # Location data of a matched token.
    token_start_offset = 0
    token_end_offset = 0
    token_start_line = 0
    token_end_line = 0
    token_start_column = 0
    token_end_column = 0

    _tokens_queue = []
    _states = []

    def __init__(self, string=None):
        if not string is None:
            self.init_string(string)

    def init_string(self, string):
        self._string = string
        self._string_len = len(string)
        self._cursor = 0
        self._tokens_queue = []

        self._states = ['INITIAL']

        self._current_line = 1
        self._current_column = 0
        self._current_line_begin_offset = 0

        # Location data of a matched token.
        self.token_start_offset = 0
        self.token_end_offset = 0
        self.token_start_line = 0
        self.token_end_line = 0
        self.token_start_column = 0
        self.token_end_column = 0

    # --------------------------------------------
    # States.

    def get_current_state(self):
        return self._states[-1]

    def push_state(self, state):
        self._states.append(state)

    # Alias for `push_state`.
    def begin(self, state):
        self.push_state(state)

    def pop_state(self):
        if len(self._states) > 1:
            return self._states.pop()

        return self._states[0]

    def get_next_token(self):
        global __, yytext, yyleng

        if len(self._tokens_queue) > 0:
            return self._to_token(self._tokens_queue.pop(0))

        if not self.has_more_tokens():
            return EOF_TOKEN

        string = self._string[self._cursor:]

        lex_rules_for_state = _lex_rules_by_conditions[self.get_current_state()]

        for lex_rule_index in lex_rules_for_state:
            lex_rule = _lex_rules[lex_rule_index]

            matched = self._match(string, lex_rule[0])

            # Manual handling of EOF token (the end of string). Return it
            # as `EOF` symbol.
            if string == '' and matched == '':
                self._cursor += 1

            if matched != None:
                yytext = matched
                yyleng = len(yytext)
                token = lex_rule[1](self)
                if token is None:
                    return self.get_next_token()

                if isinstance(token, list):
                    tokens_to_queue = token[1:]
                    token = token[0]
                    if len(tokens_to_queue) > 0:
                        self._tokens_queue.extend(tokens_to_queue)

                return self._to_token(token, yytext)

        if self.is_eof():
            self._cursor += 1
            return EOF_TOKEN

        self.throw_unexpected_token(
            string[0],
            self._current_line,
            self._current_column
        )

    def _capture_location(self, matched):
        nl_re = _syntax_tool_re.compile("\n")

        # Absolute offsets.
        self.token_start_offset = self._cursor

        # Line-based locations, start.
        self.token_start_line = self._current_line
        self.token_start_column = self.token_start_offset - self._current_line_begin_offset

        # Extract `\n` in the matched token.
        for nl_match in nl_re.finditer(matched):
            self._current_line += 1
            self._current_line_begin_offset = self.token_start_offset + nl_match.start() + 1

        self.token_end_offset = self._cursor + len(matched)

        # Line-based locations, end.
        self.token_end_line = self._current_line
        self.token_end_column = self._current_column = (self.token_end_offset - self._current_line_begin_offset)

    def _to_token(self, token_type, yytext=''):
        return {
            'type': token_type,
            'value': yytext,
            'start_offset': self.token_start_offset,
            'end_offset': self.token_end_offset,
            'start_line': self.token_start_line,
            'end_line': self.token_end_line,
            'start_column': self.token_start_column,
            'end_column': self.token_end_column,
        }

    ##
    # Throws default "Unexpected token" exception, showing the actual
    # line from the source, pointing with the ^ marker to the bad token.
    # In addition, shows `line:column` location.
    #
    def throw_unexpected_token(self, symbol, line, column):
        line_source = self._string.split('\n')[line - 1]

        pad = ' ' * column;
        line_data = '\n\n' + line_source + '\n' + pad + '^\n'

        raise Exception(
            line_data + 'Unexpected token: "' + str(symbol) + '" at ' +
            str(line) + ':' + str(column) + '.'
        )

    def is_eof(self):
        return self._cursor == self._string_len

    def has_more_tokens(self):
        return self._cursor <= self._string_len

    def _match(self, string, regexp):
        matched = _syntax_tool_re.search(regexp, string)

        if matched != None:
            self._capture_location(matched.group(0))
            self._cursor += matched.end()
            return matched.group(0)

        return None

_tokenizer = Tokenizer()


def set_tokenizer(custom_tokenizer):
    global _tokenizer
    _tokenizer = custom_tokenizer

def get_tokenizer():
    return _tokenizer

def yyloc(start, end):
    # Epsilon doesn't produce location.
    if (start is None or end is None):
        return end if start is None else start

    return {
        'start_offset': start['start_offset'],
        'end_offset': end['end_offset'],
        'start_line': start['start_line'],
        'end_line': end['end_line'],
        'start_column': start['start_column'],
        'end_column': end['end_column'],
    }

def parse(string):
    global __, __loc, yytext, yyleng

    on_parse_begin(string)

    if _tokenizer is None:
        raise Exception('_tokenizer instance wasn\'t specified.')

    _tokenizer.init_string(string)

    # Init the stack with start state 0.
    stack = [0]

    token = _tokenizer.get_next_token()
    shifted_token = None

    while True:
        if token is None:
            _unexpected_end_of_input()

        state = stack[-1]
        column = tokens[token['type']]

        if not column in table[state].keys():
            _unexpected_token(token)

        entry = table[state][column]

        # Shift.
        if entry[0] == 's':
            loc = None

            if should_capture_locations:
                loc = {
                  'start_offset': token['start_offset'],
                  'end_offset': token['end_offset'],
                  'start_line': token['start_line'],
                  'end_line': token['end_line'],
                  'start_column': token['start_column'],
                  'end_column': token['end_column'],
                }

            stack.extend((
                {
                    'symbol': tokens[token['type']],
                    'semantic_value': token['value'],
                    'loc': loc,
                },
                int(entry[1:]) # Next state.
            ))
            shifted_token = token
            token = _tokenizer.get_next_token()

        # Reduce.
        elif entry[0] == 'r':
            production = productions[int(entry[1:])]
            has_semantic_action = len(production) > 2

            semantic_value_args = None
            location_args = None

            if has_semantic_action:
                semantic_value_args = []

                if should_capture_locations:
                    location_args = []

            if production[1] != 0:
                rhs_length = production[1]

                while rhs_length > 0:
                    stack.pop()
                    stack_entry = stack.pop()

                    if has_semantic_action:
                        semantic_value_args.insert(0, stack_entry['semantic_value'])

                        if not location_args is None:
                            location_args.insert(0, stack_entry['loc'])

                    rhs_length = rhs_length - 1

            reduce_stack_entry = {'symbol': production[0]}

            if has_semantic_action:
                yytext = shifted_token != None and shifted_token['value'] or None
                yyleng = shifted_token != None and len(shifted_token['value']) or 0

                semantic_action_args = semantic_value_args

                if not location_args is None:
                    semantic_action_args = semantic_value_args + location_args

                production[2](*semantic_action_args)
                reduce_stack_entry['semantic_value'] = __

                if not location_args is None:
                    reduce_stack_entry['loc'] = __loc

                next_state = stack[-1]
                symbol_to_reduce_with = str(production[0])

            stack.extend((reduce_stack_entry, table[next_state][symbol_to_reduce_with]))

        elif entry == 'acc':
            stack.pop()
            parsed = stack.pop()

            if len(stack) != 1 or stack[0] != 0 or _tokenizer.has_more_tokens():
                _unexpected_token(token)

            if 'semantic_value' in parsed:
                on_parse_end(parsed['semantic_value'])
                return parsed['semantic_value']

            on_parse_end(True)
            return True

        if not _tokenizer.has_more_tokens() and len(stack) <= 1:
            break

def _unexpected_token(token):
    if token['type'] == EOF:
        _unexpected_end_of_input()

    _tokenizer.throw_unexpected_token(
        token['value'],
        token['start_line'],
        token['start_column']
    )

def _unexpected_end_of_input():
    _parse_error('Unexpected end of input.')

def _parse_error(message):
    raise Exception('SyntaxError: ' + str(message))


