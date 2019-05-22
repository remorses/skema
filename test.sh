
X='
Bot:
    username: Str
    competitors: [Str]
    age: Int
    friends: [Bot]
    data: InstagramData
InstagramData:
    username: Str
    password: Str
'
echo "$X" | xargs -0I%  python -m src %