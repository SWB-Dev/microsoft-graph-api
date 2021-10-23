from typing import Protocol

from ... import IGraphResponse, ISharepointList, ISharepointDocumentLibrary

class ISharepointSite(Protocol):
    
    def lists(self, list_name:str = None) -> ISharepointList:
        """"""

    def documents(self, library_name:str) -> ISharepointDocumentLibrary:
        """"""

    def get(self, url:str = None) -> IGraphResponse:
        """"""
    
    def build_url(self) -> str:
        """"""