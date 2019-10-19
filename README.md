<!--- <p align="center">
  <img width="300" src="https://github.com/remorses/mongoke/blob/master/.github/logo.jpg?raw=true">
</p> --->
<h1 align="center">skema</h1>
<h3 align="center">Single source of truth for all your types</h3>



## Examples

## Nested objects
```yml
User:
    id: Int
    name: Str
    address:
        street: Str
        number: Int
        state: Str
    credit: Float
    email: /.*@.*\.com/
```

## Lists
```yml
Pet:
    name: Str
    friends: [Pet] # you can reference other types

Owner:
    full_name: Str
    hobbies: [
        name: Str
        when: CronString
    ]

CronString: Str
```

## Unions
```yml
Animal: Tiger | Bear | Panthera

Panthera:
    _id: ObjectId # a type alias
    black_nuance: "super_dark" | "dark" | "light" # enumeration

Tiger:
    _id: ObjectId
    humans_killed: Int

Bear:
    _id: ObjectId
    likes_honey: Bool

ObjectId: Any
```

## And types
```yml
Centaur: Horse & Human

Horse:
    name: Str
    eats: ["carrots" | "weeds"]

Human:
    name: Str
    surname: Str
    eats: ["meat" | "vegetables"]
```





## Built in types
- Int
- Float
- Str
- Bool
- null
- "literal string"
- /regex/
- 0..69
- Any



## What you can do with a skema file:
- Validate json input
- Generare code types for every language in your architecture (graphql, py, ts, cpp, ...)
- Generate fake data based on your schema
- Infer schema from raw json (perfect for reverse engineering)
- convert jsonschema to be easier to read
- use it for API types documentation
- Generate react forms, via [`react-skema-forms`]
- use it to plan your domain model!


## spec

- all root properties are references and can be used as types
- types can be object whose properties are expressed as key: value or other primitive types like 
    - Str,
    - Int,
    - Bool,
    - Float
    - /regex/
    - 0..100 (int range)
    - .0..1 (float range)
- type inside [ ] is an array type
- types can be mixed together: 
    - `Str | Int` means one of string and int
    - `Object1 & Object2` means "all the properties of object 1 and 2"
    - `Object1 | Object2` means "properties of object 1 and 2"
- types can be annotated writing annotations """ quotes above the definition
- additional propertiescan be specified adding ... at the end of an object and can be better shaped treating it like a normal key, ...: Str means additional properties must be Str


## todo:
- optional types are union of null ans the type in jsonschema
- scalar name can be overridden by other splitted types in py and gql
- when generating python i have to order dependencies over the types
- ~~scalar unions with null should be removed from graphql~~
- --hide [...] should support other types than scalars and opther lans other than gql
- ~~specify if a type gets translated as input, interface in graphql, [graphql input]
- spaces between properties cause properties spaced to be taken at an outer level
- graphql doesn't support union inside unions, so i must unnest them
- in graphql enums with options > 2 are taken as strings
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
