from __future__ import annotations
from typing import Protocol

class IGraphFilter(Protocol):

    def add_subfilter(self, filter:IGraphFilter):
        """"""
    
    def compose(self) -> str:
        """"""