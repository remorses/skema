({
    lex: {
        rules: [
            // 
            [`[a-zA-Z0-9_]+:[ ]*`, `
            last = len(yytext.strip()) - 1
            yytext = yytext[0:last]
            return 'REQUIRED_KEY'
            `],
            // 
            ["\\[", "return '['"],
            ["\\]", "return ']'"],

            [`[a-zA-Z0-9_]+:\\?`, `
            yytext = yytext[0: len(yytext) - 2]
            return 'OPTIONAL_KEY'
            `],
    
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