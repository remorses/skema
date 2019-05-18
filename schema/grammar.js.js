({
    lex: {
        rules: [
            // 
            [`[a-zA-Z0-9_]+:`, `
            yytext = yytext.slice(0, yytext.length - 1);
            return 'KEY'
            `],
    
            [`[a-zA-Z0-9_]+`, `return 'VAL'`],
    
            ["\\[", "return '['"],
            ["\\]", "return ']'"],
    
    
            ["\\.\\.\\.", "return 'ADDITIONAL_PROPERTIES'"],
            // ------------------------------------------------
            // Indent/Dedent.
    
            [`\\n( *)`, `
      
            yytext = yytext.slice(1); // strip leading NL
            yytext = yytext.length;
    
            return 'SEPARATOR';
            `],
    
            [`\\s+`, `/* skip whitespace */`],
            // [`:`,    `/* skip whitespace */`],
            // [`\\-`,     `return '-'`],
        ],
    },
    bnf: {
        Entry:   [[`VAL`,  `$$ = $2`]],
    }
})