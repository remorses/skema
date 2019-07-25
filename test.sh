# cd ~
X='
x:
    a: Int
    b: C
    obj: any
C: Str
any:
    ...
'
echo "$X" | python -m skema