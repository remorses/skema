from skema import dictlike
from typing import Optional, List, Any, Union
from typing_extensions import Literal

SchemaTypeEnums = Union[Literal["string"], Literal["array"], Literal["object"], Literal["number"], Literal["boolean"], Literal["integer"]]
SchemaTypeEnums.from_ = lambda x: x

SchemaType = Union["SchemaTypeEnums", List["SchemaTypeEnums"]]
SchemaType.from_ = lambda x: x

Block = Union["GenericBlock", "Enum", "Object", "Array", "Constant", "AllOf", "AnyOf", "OneOf"]
Block.from_ = lambda x: x

class Object(dictlike):
    
    type: "SchemaType"
    properties: Any
    additionalProperties: Any
    
    def __init__(
        self,
        *, 
        type,
        properties,
        additionalProperties, 
        **kwargs
    ):
        super().__init__(
            type=SchemaType.from_(type) if type != None else None,
            properties=properties if properties != None else None,
            additionalProperties=additionalProperties if additionalProperties != None else None,
            **kwargs
        )

class GenericBlock(dictlike):
    
    type: "SchemaType"
    
    def __init__(
        self,
        *, 
        type, 
        **kwargs
    ):
        super().__init__(
            type=SchemaType.from_(type) if type != None else None,
            **kwargs
        )

class Enum(dictlike):
    
    enum: List["Block"]
    
    def __init__(
        self,
        *, 
        enum, 
        **kwargs
    ):
        super().__init__(
            enum=[Block.from_(x) for x in enum] if enum != None else None,
            **kwargs
        )

class Constant(dictlike):
    
    const: str
    
    def __init__(
        self,
        *, 
        const, 
        **kwargs
    ):
        super().__init__(
            const=str(const) if const != None else None,
            **kwargs
        )

class AllOf(dictlike):
    
    allOf: List["Block"]
    
    def __init__(
        self,
        *, 
        allOf, 
        **kwargs
    ):
        super().__init__(
            allOf=[Block.from_(x) for x in allOf] if allOf != None else None,
            **kwargs
        )

class AnyOf(dictlike):
    
    anyOf: List["Block"]
    
    def __init__(
        self,
        *, 
        anyOf, 
        **kwargs
    ):
        super().__init__(
            anyOf=[Block.from_(x) for x in anyOf] if anyOf != None else None,
            **kwargs
        )

class OneOf(dictlike):
    
    oneOf: List["Block"]
    
    def __init__(
        self,
        *, 
        oneOf, 
        **kwargs
    ):
        super().__init__(
            oneOf=[Block.from_(x) for x in oneOf] if oneOf != None else None,
            **kwargs
        )

class Array(dictlike):
    
    items: "Block"
    
    def __init__(
        self,
        *, 
        items, 
        **kwargs
    ):
        super().__init__(
            items=Block.from_(items) if items != None else None,
            **kwargs
        )
