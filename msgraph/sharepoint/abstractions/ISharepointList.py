from typing import Protocol, Callable

from ... import IGraphResponse, IGraphFilter, IGraphAction
from .ISharepointListItem import ISharepointListItem

class ISharepointList(Protocol):
    def item(self, id:int) -> ISharepointListItem:
        """"""
    
    def items(self) -> ISharepointListItem:
        """"""

    def filters(self, filter_func:Callable[...,list[IGraphFilter]]) -> IGraphAction:
        """"""

    def columns(self) -> IGraphAction:
        """"""
    
    def content_types(self) -> IGraphAction:
        """"""

    def created_by_user(self) -> IGraphAction:
        """"""

    def last_modified_user(self) -> IGraphAction:
        """"""

    def subscriptions(self) -> IGraphAction:
        """"""

    def get(self, url:str = None) -> IGraphResponse:
        """"""
    
    def get_all(self):
        """"""
    
    def build_url(self) -> str:
        """"""