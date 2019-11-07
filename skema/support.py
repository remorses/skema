class modifiers:
    GRAPHQL_INPUT = "[graphql input]"
    GRAPHQL_HIDDEN = "[graphql hide]"


class types:
    STR = "type_str"
    BOOL = "type_bool"
    ANY = "type_any"
    INT = "type_int"
    FLOAT = "type_float"
    REGEX = "regex"


class literals:
    NULL = "literal_null"
    TRUE = "literal_true"
    FALSE = "literal_false"
    STRING = "literal_string"
    INTEGER = "literal_integer"
    ELLIPSIS = "literal_ellipsis"


class composed_types:
    OBJECT = "object"
    LIST = "list"
    INTERSECTION = "intersection"
    UNION = "union"
    RANGE = "bounded_range"
    LOW_RANGE = "low_bounded_range"
    HIGH_RANGE = "high_bounded_range"


class structure:
    START = "start"
    ROOT_PAIR = "root_pair"
    REQUIRED_PAIR = "required_pair"
    OPTIONAL_PAIR = "optional_pair"
    REFERENCE = "reference"
    ANNOTATION = "annotation"


def capitalize(s: str):
    if not s:
        return ""
    return s[0].capitalize() + s[1:]
