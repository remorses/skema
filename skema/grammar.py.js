({
    lex: {
        rules: [
            ['"""(?:(?!""").|\n)*"""[ ]*', `
            last = len(yytext.strip()) - 3
            yytext = yytext[3:last]
            return 'ANNOTATION'
            `],

            ['/.*/', `
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



            ["\\[", "return '['"],
            ["\\]", "return ']'"],

    
            [`[a-zA-Z0-9_&\\| "]+`, `return 'VAL'`],
            // [`[a-zA-Z0-9_]+`, `return 'VAL'`],
    


            // ["&", "return '&'"],
    
    
            ["\\.\\.\\.", "return '...'"],
            // ------------------------------------------------
            // Indent/Dedent.
    
            [`\\n( *)`, `
      
            yytext = yytext[1:]
            yytext = len(yytext)
    
            return 'SEPARATOR'
            `],
    
            [`\\s+`, `pass`],
            // [`:`,    `/* skip whitespace */`],
            // [`\\-`,     `return '-'`],
        ],
    },
    bnf: {
        Entry:   [[`VAL`,  `$$ = $2`]],
    }
})