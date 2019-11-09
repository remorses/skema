from skema.lark import Tree, Token


class UniqueKey(Token):
    type: str
    value: str
    pos_in_stream: str
    line: str
    column: str
    end_line: str
    end_column: str

    def __new__(cls, token):
        self = Token.__new__(
            cls,
            token.type,
            token.value,
            token.pos_in_stream,
            token.line,
            token.column,
            token.end_line,
            token.end_column,
        )
        return self

    def __repr__(self):
        return f"`{self.value}`"

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return str.__hash__(f"{self.column}{self.line}{self.value}")
