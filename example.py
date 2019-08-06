from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Object:
    a_ciao: Optional[float]
    b_com: str
    sdf: Optional[float]


@dataclass
class Posts:
    name: str
    url: str


@dataclass
class Campaign:
    """Descrizione PostCampaign
    
    Descrizione Node
    
    Descrizione della camp
    
    Descrizione MessageOwn
    """
    label: str
    y: float
    """Descrizione name"""
    name: str
    posts: Optional[List[Posts]]
    """Descrizione della prop"""
    x: Optional[float]


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
    """Descrizione della prop"""
    x: float


@dataclass
class MessageCampaign:
    """Descrizione della camp
    
    Descrizione MessageOwn
    """
    label: str
    y: float
    name: str


@dataclass
class MessageOwn:
    """Descrizione MessageOwn"""
    name: str
