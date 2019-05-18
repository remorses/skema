({
    lex: {
        rules: [
            // 
            [`[a-zA-Z0-9_]+:`, `
            yytext = yytext[0: len(yytext) - 1]
            return 'KEY'
            `],
    
            [`[a-zA-Z0-9_]+`, `return 'VAL'`],
    
            ["\\[", "return '['"],
            ["\\]", "return ']'"],
    
    
            ["\\.\\.\\.", "return 'ADDITIONAL_PROPERTIES'"],
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