from random import randint

from hypothesis import strategies as hs
# from hypothesis._strategies import from_regex as regex
import json
from .regex import regex


def gen_int(prop):
    min_value = prop.get("minimum", 0)
    max_value = prop.get("maximum", 1000)
    return hs.integers(min_value=min_value, max_value=max_value)


def gen_string(prop):
    min_value = prop.get("minLength", 5)
    max_value = prop.get("maxLength", 30)
    pattern = prop.get('pattern', r'[ A-Za-z\d]+')
    return regex(pattern, )\
            .filter(lambda x: min_value <= len(x) and len(x) <= max_value)\
            .map(lambda x: x.rstrip('\x00'))
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


def gen_array(prop, customs):
    min_items = prop.get("minItems", 0)
    max_items = prop.get("maxItems", 5)
    if prop.get("items", {}).get("type", False) is not False:
        generator = get_generator(prop.get("items"), customs)
        return hs.lists(elements=generator,
                        min_size=min_items,
                        max_size=max_items)
    return hs.lists(elements=gen_anything(),
                    min_size=min_items,
                    max_size=max_items)


def gen_anything():
    return hs.one_of(gen_int({}), gen_string({}), hs.booleans(), hs.none())

def gen_json_values():
    return gen_string({}) | hs.booleans() | gen_int({}) | hs.none() | hs.floats(allow_nan=False, allow_infinity=False)

def gen_any_obj():
    return hs.recursive(hs.dictionaries(gen_string({}), gen_json_values()),
                        lambda children: hs.dictionaries(gen_string({}), children),
                        max_leaves=10)

def gen_object(prop, customs):

    required = prop.get("required", [])
    output = {}
    prop_key = "properties"
    if prop.get("properties", None) is None:
        if prop["additionalProperties"]:
            return gen_any_obj()

    for k in prop[prop_key].keys():
        json_prop = prop[prop_key][k]

        if should_include(k, required):
            output[k] = get_generator(json_prop, customs)


    return hs.fixed_dictionaries(output)


def gen_enum(prop):
    enum = prop["enum"]
    return hs.sampled_from(enum)

def gen_const(prop):
    const = prop["const"]
    return hs.just(const)

def gen_bool(prop):
    return hs.booleans()

def gen_one_of(prop, customs):
    possible_values = []
    for value in prop["oneOf"]:
        possible_values.append(get_generator(value), customs)

    return hs.one_of(possible_values)

def gen_any_of(prop, customs):
    possible_values = []
    for value in prop["anyOf"]:
        possible_values.append(get_generator(value, customs))

    return hs.one_of(possible_values)

specials = ['allOf', 'oneOf', 'anyOf']

def merge_all_of(prop,):
    dicts = prop["allOf"]

    if not all([any([x in d for x in specials]) or d.get('type') == 'object'  for d in dicts]):
        raise Exception(f'allOf is supported as array of object types: {json.dumps(dicts, indent=4, default=repr)}')
    result = {
        'additionalProperties': True,
        'required': [],
        'properties': {},
    }
    for obj in dicts:
        if 'allOf' in obj:
            obj = merge_all_of(obj)
    
        result['additionalProperties'] = result['additionalProperties'] and bool(obj.get('additionalProperties', True))
        result['properties'] = {**result['properties'], **(obj.get('properties', {}) or {})}
        result['required'] = result['required'] + (obj.get('required', [])  or [])
    result['required'] = list(set(result['required']))
    return result

def gen_all_of(prop, customs):
    result = merge_all_of(prop)
    return gen_object(result, customs)

def get_generator(prop, customs={}):
    disp = {"string": gen_string,
            "integer": gen_int,
            "number": gen_int,
            "boolean": gen_bool,
            
    }
    if prop.get('title') != None:
        title = prop.get('title', '').strip()
        if title in customs:
            # print(customs[title]())
            return hs.builds(lambda x: customs[title](), hs.integers())
        else:
            prop = {k:v for k,v in prop.items() if k != 'title' and k != 'description'}
    
    if not prop:
        return gen_anything()

    enum = prop.get("enum", None)
    if enum is not None:
        return gen_enum(prop)

    if 'const' in prop:
        return gen_const(prop)

    one_of = prop.get("oneOf", None)
    if one_of is not None:
        return gen_one_of(prop, customs)

    any_of = prop.get("anyOf", None)
    if any_of is not None:
        return gen_any_of(prop, customs)

    all_of = prop.get("allOf", None)
    if all_of is not None:
        return gen_all_of(prop, customs)

    if 'object' == prop.get('type'):
        return gen_object(prop, customs)

    if 'array' == prop.get('type'):
        return gen_array(prop, customs)

    json_type = prop.get("type", None)
    if json_type is None:
        raise JsonTypeError("Couldnt find type in prop {0}".format(prop))

    return disp[json_type](prop)



class JsonTypeError(Exception):
    pass
