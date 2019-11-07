<p align="center">
  <img width="350" src="https://github.com/remorses/skema/blob/lark/.github/logo.gif?raw=true">
</p>
<h1 align="center">skema</h1>
<h3 align="center">Single source of truth for all your types</h3>

## Todo 
- multiple interfaces not supported in grammar


## Why

Today multi-service architectures requires developers to keep in sync a lot of different services built in different languages by different teams.
To do this manually requires a lot of work always changing the shared object types between different projects and a lot of integration tests to make sure that all the services can communicate.
With skema you can have one single source of truth for your most important shared types and can generate the validation (jsonschema) and the code to serialize them and be sure the different services can communicate.

## Supported languages
### built-in
- **jsonschema**
- **python**
- **graphql**
### using [quicktype](https://github.com/quicktype/quicktype)
- **python**
- **typescript**
- **go**
- **rust**
- **c++**
...

## Installation
Requires python 3.6+ and npm
```
pip install skema
npm i -g quicktype # for more languages
```

## Usage
```
skema generate ./schema.skema --jsonschema ./your_path.json
skema generate ./schema.skema --graphql ./your_path.graphql
skema generate ./schema.skema --typescript ./your_path.graphql
# using an hosted skema
skema generate "https://gist.github.com/your_gist" --typescript ./your_path.graphql
```


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

