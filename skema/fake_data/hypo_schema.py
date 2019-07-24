from random import randint

from hypothesis import strategies as hs

from .regex import regex


def gen_int(prop):
    min_value = prop.get("minimum", 0)
    max_value = prop.get("maximum", 1000)
    return hs.integers(min_value=min_value, max_value=max_value)


def gen_string(prop):
    min_value = prop.get("minLength", 5)
    max_value = prop.get("maxLength", 30)
    pattern = prop.get('pattern', '[ A-Za-z\d]+')
    return hs.just(regex(pattern).filter(lambda x: min_value <= len(x) and len(x) <= max_value).example())
    # return hs.text(
    #     hs.characters(
    #         max_codepoint=100, 
    #         blacklist_categories=('Cc', 'Cs')),
    #         min_size=min_value, 
    #         max_size=max_value
    #     ).map(lambda s: s.strip()
    # ).filter(lambda s: len(s) > 0)



def should_include(key, required_list):
    if key in required_list:
        return True
    else:
        return bool(randint(0, 1))


def gen_array(prop):
    min_items = prop.get("minItems", 0)
    max_items = prop.get("maxItems", 5)
    if prop.get("items", {}).get("type", False) is not False:
        generator = get_generator(prop.get("items"))
        return hs.lists(elements=generator,
                        min_size=min_items,
                        max_size=max_items)
    return hs.lists(elements=gen_anything(),
                    min_size=min_items,
                    max_size=max_items)


def gen_anything():
    return hs.one_of(gen_int({}), gen_string({}), hs.booleans(), hs.none())

def gen_json_values():
    return hs.text() | hs.booleans() | hs.integers() | hs.none() | hs.floats()

def gen_any_obj():
    return hs.recursive(hs.dictionaries(hs.text(), gen_json_values()),
                        lambda children: hs.dictionaries(hs.text(), children),
                        max_leaves=10)

def gen_object(prop):

    required = prop.get("required", [])
    output = {}
    prop_key = "properties"
    if prop.get("properties", None) is None:
        if prop["additionalProperties"] is True or prop["additionalProperties"] == {}:
            return gen_any_obj()
        return hs.dictionaries(hs.text(min_size=1),
                               get_generator(prop["additionalProperties"]))

    for k in prop[prop_key].keys():
        json_prop = prop[prop_key][k]

        if should_include(k, required):
            output[k] = get_generator(json_prop)

    return hs.fixed_dictionaries(output)


def gen_enum(prop):
    enum = prop["enum"]
    return hs.sampled_from(enum)

def gen_const(prop):
    const = prop["const"]
    return hs.sampled_from([const])

def gen_bool(prop):
    return hs.booleans()

def gen_one_of(prop):
    possible_values = []
    for value in prop["oneOf"]:
        possible_values.append(get_generator(value))

    return hs.one_of(possible_values)

def gen_any_of(prop):
    possible_values = []
    for value in prop["anyOf"]:
        possible_values.append(get_generator(value))

    return hs.one_of(possible_values)

def gen_all_of(prop):
    dicts = prop["allOf"]
    if not all([d['type'] == 'object' for d in dicts]):
        raise Exception('allOf is supported as array of object types')
    result = {
        'additionalProperties': True,
        'required': [],
        'properties': {},
    }
    for obj in dicts:
        result['additionalProperties'] = result['additionalProperties'] and bool(obj.get('additionalProperties', True))
        result['properties'] = {**result['properties'], **(obj.get('properties', {}) or {})}
        result['required'] = result['required'] + (obj.get('required', [])  or [])
    result['required'] = list(set(result['required']))
    return gen_object(result)




def get_generator(prop):
    disp = {"string": gen_string,
            "integer": gen_int,
            "number": gen_int,
            "boolean": gen_bool,
            "object": gen_object,
            "array": gen_array,
    }
    if not prop:
        return gen_anything()

    enum = prop.get("enum", None)
    if enum is not None:
        return gen_enum(prop)

    const = prop.get("const", None)
    if const is not None:
        return gen_const(prop)

    one_of = prop.get("oneOf", None)
    if one_of is not None:
        return gen_one_of(prop)

    any_of = prop.get("anyOf", None)
    if any_of is not None:
        return gen_any_of(prop)

    all_of = prop.get("allOf", None)
    if all_of is not None:
        return gen_all_of(prop)

    json_type = prop.get("type", None)
    if json_type is None:
        raise JsonTypeError("Couldnt find type in prop {0}".format(prop))

    return disp[json_type](prop)

def generate_from_schema(json_schema):
    example_data = get_generator(json_schema)
    return example_data


class JsonTypeError(Exception):
    pass
