({
    lex: {
        rules: [
            ['"""(?:(?!""").|\\n)*"""[ ]*', `
            last = len(yytext.strip()) - 3
            yytext = yytext[3:last]
            if yytext and yytext[0] == '\\n':
                yytext = yytext[1:]
            if yytext and yytext[-1] == '\\n':
                yytext = yytext[:-1]
            return 'ANNOTATION'
            `],

            ['/.*/[ ]*', `
            last = len(yytext.strip()) - 1
            yytext = yytext[1:last]
            return 'REGEX'
            `],

            [`[a-zA-Z0-9_]+\\?:[ ]*`, `
            last = len(yytext.strip()) - 2
            yytext = yytext[0:last]
            return 'OPTIONAL_KEY'
            `],

            [`[a-zA-Z0-9_]+:[ ]*`, `
            last = len(yytext.strip()) - 1
            yytext = yytext[0:last]
            return 'REQUIRED_KEY'
            `],



            ["\\[[ ]*", "return '['"],
            ["\\][ ]*", "return ']'"],

            ["\\.\\.\\.[ ]*", "return '...'"],
    
            [`[a-zA-Z0-9_&\\| !."]+`, `
            # print('token_start_column', self.token_start_column)
            # yytext = yytext.replace('!', '')
            yytext = yytext.strip()
            if self.token_start_column == 0:
                last = len(yytext.strip()) - 1
                yytext = yytext[1:last]
                return 'ANNOTATION'
            else:
                return 'VAL'
            `],
            // [`[a-zA-Z0-9_]+`, `return 'VAL'`],
    


            // ["&", "return '&'"],
    
    
            
            // ------------------------------------------------
            // Indent/Dedent.
    
            [`\\n((?:[ ]|#.*)*)`, `
            if '#' in yytext:
                pass
            else:
                yytext = yytext[1:]
                yytext = len(yytext)
                return 'SEPARATOR'
            `],
            [`#.*`, `pass`],
            [`\\s+`, `pass`],
            
            // [`:`,    `/* skip whitespace */`],
            // [`\\-`,     `return '-'`],
        ],
    },
    bnf: {
        Entry:   [[`VAL`,  `$$ = $2`]],
    }
})