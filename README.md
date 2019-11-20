<p align="center">
  <img width="450" src="https://raw.githubusercontent.com/remorses/skema/master/.github/skema_logo.jpg">
</p>
<!-- <h1 align="center">skema</h1> -->
<h3 align="center">Single source of truth for all your types</h3>

<a href="https://skema.club/">Site</a> • <a href="https://skema.club/app/">Playground</a> • <a href="https://skema.club/docs/">Docs</a>

## Why

Today multi-service architectures requires developers to keep in sync a lot of different services built in different languages by different teams.
Doing this manually requires a lot of work always changing the shared object types between different projects and a lot of integration tests to make sure that all the services can communicate.
With skema you can have one single source of truth for your shared types and have static checkers warn you when some services use different shared types.

## Supported target languages

-   **jsonschema**
-   **python**
-   **graphql**
-   **typescript**

## Soon

adding other languages support is pretty straightforward

-   **go**
-   **rust**
-   **sql**
    ...

## Installation

Requires python 3.6+

```
pip install skema
```

# Usage

```sh
# Generating types
cat ./schema.skema | skema to python > types.py
cat ./schema.skema | skema to typescript > types.ts
cat ./schema.skema | skema to jsonschema > types.json
# From jsonschema to graphql
cat ./schema.json | skema from jsonschema | skema to graphql > ./schema.graphql
# From graphql to python
cat ./schema.graphql | skema from graphql | skema to python > ./types.py
# Use your imagination
```

---

# Examples

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
    email: Str
```

## Lists

```yml
CronString: Str

Pet:
    name: Str
    friends: [Pet] # you can reference other types

Owner:
    full_name: Str
    hobbies: [
        name: Str
        when: CronString
    ]


```

## Unions

```yml
Animal: Tiger | Bear | Panthera

ObjectId: Any

Panthera:
    _id: ObjectId # a type alias
    black_nuance: "super_dark" | "dark" | "light" # enumeration

Tiger:
    _id: ObjectId
    humans_killed: Int

Bear:
    _id: ObjectId
    likes_honey: Bool
```

## And types

```yml
Centaur: Horse & Human

Horse:
    name: Str
    eats: "carrots" | "weeds"

Human:
    name: Str
    surname: Str
    eats: "meat" | "vegetables"
```

## Built in types

-   Int
-   Float
-   Str
-   Bool
-   null
-   "literal string"
-   /regex/
-   0 .. 69 (ranges)
-   Any

## What you can do with a skema file:

-   Validate json input
-   Generare code types for every language in your architecture (graphql, py, ts, ...)
-   Generate fake data based on your schema
-   Infer schema from raw json (perfect for reverse engineering)
-   convert jsonschema to be easier to read
-   use it for API types documentation
-   Generate react forms
-   use it to plan your domain model!

## spec

-   all root properties are references and can be used as types
-   types can be object whose properties are expressed as key: value or other primitive types like
    -   Str,
    -   Int,
    -   Bool,
    -   Float
    -   /regex/
    -   0 .. 100 (int range)
    -   .0 .. 1 (float range)
-   type inside [ ] is an array type
-   types can be mixed together:
    -   `Str | Int` means one of string or int
    -   `Object1 & Object2` means "all the properties of object 1 and 2"
    -   `Object1 | Object2` means "properties of object 1 or 2"
-   types can be annotated writing annotations """\nannotation\n""" quotes above the definition
-   you can use ... to mean that additional properties can be added to an object
