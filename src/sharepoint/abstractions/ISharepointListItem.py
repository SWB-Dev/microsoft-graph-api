from typing import Protocol, Callable

from ... import IGraphAction, IGraphFilter

class ISharepointListItem(Protocol):
    def filters(self, filter_func:Callable[...,list[IGraphFilter]]) -> IGraphAction:
        """"""

    def count(self) -> IGraphAction:
        """"""
    
    def batch(self, data:list[dict]) -> IGraphAction:
        """"""