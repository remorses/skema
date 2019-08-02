LIST = '[]'
AND = '&'
OR = '|'
ANY = 'Any'
INT = 'Int'
STR = 'Str'
STRING = 'String'
REGEX = '//'
FLOAT = 'Float'
NULL = 'null'
BOOL = 'Bool'
ELLIPSIS = '...'

constants = [globals()[v] for v in globals() if not v.startswith('_')]
