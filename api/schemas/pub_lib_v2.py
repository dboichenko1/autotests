from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel


class LibInfo(BaseModel):
    user: str
    userId: int
    scriptIdPart: str
    version: str
    docs: str
    chartId: str
    isPublic: bool
    lib: str
    libId: str


class Arg(BaseModel):
    allowedTypeIDs: List[str]
    displayType: str
    name: str
    required: bool
    desc: Optional[str] = None
    desc: Optional[str] = None


class Function(BaseModel):
    args: List[Arg]
    libId: str
    name: str
    returnedTypes: List[str] = None
    syntax: List[str]
    thisType: Optional[List[str]] = None
    desc: Optional[List[str]] = None
    returns: Optional[List[str]] = None


class Field(BaseModel):
    desc: List[str] = None
    desc: List[Optional[str]] = None
    name: str
    type: str


class Type(BaseModel):
    desc: List[str] = None
    fields: List[Field]
    libId: str
    name: str


class Exports(BaseModel):
    functions: List[Function]
    types: List[Type]


class Model_v2(BaseModel):
    libInfo: LibInfo
    exports: Exports
