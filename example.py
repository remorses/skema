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
    label: str
    x: float
    y: float
    name: str
    posts: Optional[List[Posts]]


@dataclass
class Base:
    label: str
    x: float
    y: float


@dataclass
class Node:
    name: str


@dataclass
class PostCampaign:
    label: str
    x: float
    y: float
    name: str
    posts: List[Posts]


@dataclass
class MessageCampaign:
    label: str
    x: float
    y: float
    name: str


@dataclass
class MessageOwn:
    name: str
