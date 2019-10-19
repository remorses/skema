
## todo:
- optional types are union of null and the type in jsonschema
- scalar name can be overridden by other splitted types in py and gql
- ~~when generating python i have to order dependencies over the types~~
- ~~scalar unions with null should be removed from graphql~~
- --hide [...] should support other types than scalars and opther lans other than gql
- ~~specify if a type gets translated as input, interface in graphql, [graphql input]
- spaces between properties cause properties spaced to be taken at an outer level
- graphql doesn't support union inside unions, so i must unnest them
- in graphql enums with options ==1 or > 2 are taken as strings
- if i use Root as a name, this is removed from graphql
- when using from_jsonschema the i have to dereference anyOf, oneOf, allOf and enums. These can share same name (parent.value + property) and can conflict in final skema
- when dereferencing skema to produce graphql i am adding parent  names to differentiate the final type names, i am not sure this can really work in long term
- when creating python code, special keywords (from) are padded with parent names, this means i can't use `ObjectName(**data)`
- python code translates const enums as an enum object of a single value, it should search for other equal common enum ref (can be solved using common interface)
- | and & don't work with [], because VAl is split with ARRAY and smaller VAL during tokenization, is hould add a rule during tokenization to exclude | and & in array tokens and add array logic inside VAL handling (can be solved putting [] only to a reference)
- the same for regex
- better handling of comments and white space
- dynamic indentation (now is set as 4 spaces)
- ~~in gql remove types used in & operations, given that thay are merged~~





bugs:
- if key name is equal to another type name then fuck it up
- can't write `key: [Str] | Int`
- objects get additionalProps: true by default even if they haven't ... at the end like:
```
Object:
    a: Str
    b: Int
    ...
```
this is because i always forget to put them when doing `Object1 & Object2` so i just removed it



graphql todos:
- remove useless parent nesting in names if possible
- assert no other types exist before generating one
- customization for Interface_end_name, 
