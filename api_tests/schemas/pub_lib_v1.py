from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field

"""v1"""
class LibInfo(BaseModel):
    user: str #= Field(le =1) так можно провалидировать
    userId: int
    scriptIdPart: str
    version: str
    docs: str
    chartId: str
    isPublic: bool
    lib: str
    libId: str


class Arg(BaseModel):
    name: str
    type: str
    info: Optional[str] = None


class Doc(BaseModel):
    args: List[Arg]
    name: str
    syntax: str
    thisType: Optional[List[str]] = None
    desc: Optional[str] = None
    returnType: Optional[str] = None


class Functions2Item(BaseModel):
    docs: List[Doc]
    prefix: str
    title: str


class Field(BaseModel):
    desc: str
    name: str
    type: str


class Doc1(BaseModel):
    desc: str
    fields: List[Field]
    name: str


class Type(BaseModel):
    docs: List[Doc1]
    prefix: str
    title: str


class Exports(BaseModel):
    functions2: List[Functions2Item]
    types: List[Type]


class Model_V1(BaseModel):
    libInfo: LibInfo
    exports: Exports

