const { parse } = require("./parser.js")

const parsed = parse(`
- entry1:             # INDENT
- entry11           # NL
- entry12           # NL
- entry13:          # INDENT
  - entry131        # NL
  - entry131        # NL
  - entry133:       # INDENT
    - entry1331     # NL
    - entry1332     # DEDENT, DEDENT, NL
- entry2
`.trim())

print(JSON.stringify(parsed, null, '    '))


