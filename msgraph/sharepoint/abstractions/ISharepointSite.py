from typing import Protocol, Callable

from ... import IGraphResponse, IGraphFilter, IGraphAction

from .ISharepointDocumentLibrary import ISharepointDocumentLibrary
from .ISharepointList import ISharepointList

class ISharepointSite(Protocol):
    
    def lists(self, list_name:str = None) -> ISharepointList:
        """"""

    def filters(self, filter_func:Callable[...,list[IGraphFilter]]) -> IGraphAction:
        """"""

    def documents(self, library_name:str) -> ISharepointDocumentLibrary:
        """"""

    def get(self, url:str = None) -> IGraphResponse:
        """"""
    
    def build_url(self) -> str:
        """"""