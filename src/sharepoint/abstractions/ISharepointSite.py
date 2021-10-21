from typing import Protocol

from ... import ISharepointList, ISharepointDocumentLibrary

class ISharepointSite(Protocol):
    
    def lists(self, list:str) -> ISharepointList:
        """"""

    def documents(self, library_name:str) -> ISharepointDocumentLibrary:
        """"""

    def get(self, url:str = None):
        """"""
    
    def build_url(self) -> str:
        """"""