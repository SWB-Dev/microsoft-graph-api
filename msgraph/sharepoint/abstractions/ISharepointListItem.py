from typing import Protocol, Callable

from ... import IGraphResponse, IGraphAction, IGraphFilter

class ISharepointListItem(Protocol):
    def filters(self, filter_func:Callable[...,list[IGraphFilter]]) -> IGraphAction:
        """"""

    def count(self) -> IGraphAction:
        """"""
    
    def batch(self, data:list[dict]) -> IGraphAction:
        """"""
    
    def get(self, url:str = None) -> IGraphResponse:
        """"""