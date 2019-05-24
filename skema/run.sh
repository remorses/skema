cd `dirname $0`
# syntax-cli --lex ./indent.js  --mode slr1 -f ./indent.txt
# syntax-cli --lex ./lex.js  --mode slr1 --tokenize -f ./test.txt
# syntax-cli --lex ./lex.js  --mode slr1  -o ./parser.js
# syntax-cli -l ./lex.js  --mode slr1 -o ./parser.py
# syntax-cli -g ./grammar.py.js  --mode slr1 -o ./parser.py
syntax-cli -g ./grammar.py.js  --mode slr1  -o ./parser.py