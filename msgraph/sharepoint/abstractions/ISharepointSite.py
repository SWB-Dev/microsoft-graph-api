from typing import Protocol

from ... import IGraphResponse, ISharepointList, ISharepointDocumentLibrary

class ISharepointSite(Protocol):
    
    def lists(self, list:str) -> ISharepointList:
        """"""

    def documents(self, library_name:str) -> ISharepointDocumentLibrary:
        """"""

    def get(self, url:str = None) -> IGraphResponse:
        """"""
    
    def build_url(self) -> str:
        """"""