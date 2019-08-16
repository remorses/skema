from dataclasses import dataclass
from typing import Optional, List


@dataclass
class X:
    x: str


@dataclass
class GenericEdge:
    cose: X


@dataclass
class Root:
    x: GenericEdge


@dataclass
class A:
    x: str


@dataclass
class B:
    x: str


@dataclass
class C:
    x: str


@dataclass
class D:
    x: str


@dataclass
class E:
    x: str


@dataclass
class Object:
    b_com: str
    a_ciao: Optional[float] = None
    sdf: Optional[float] = None


@dataclass
class Posts:
    name: str
    url: str


@dataclass
class Campaign:
    """Descrizione Campaign
    
    
    
    Descrizione PostCampaign
    
    Descrizione Node
    
    Descrizione MessageCampaign
    
    Descrizione MessageOwn
    """
    label: str
    y: float
    """Descrizione name"""
    name: str
    posts: Optional[List[Posts]] = None
    """Descrizione x"""
    x: Optional[float] = None


@dataclass
class Base:
    label: str
    y: float


@dataclass
class Node:
    """Descrizione Node"""
    """Descrizione name"""
    name: str


@dataclass
class PostCampaign:
    """Descrizione PostCampaign
    
    Descrizione Node
    """
    label: str
    y: float
    """Descrizione name"""
    name: str
    posts: List[Posts]
    """Descrizione x"""
    x: float


@dataclass
class MessageCampaign:
    """Descrizione MessageCampaign
    
    Descrizione MessageOwn
    """
    label: str
    y: float
    name: str


@dataclass
class MessageOwn:
    """Descrizione MessageOwn"""
    name: str
