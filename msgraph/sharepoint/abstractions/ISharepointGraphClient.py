from typing import Protocol

from .ISharepointGraphRequest import ISharepointGraphRequest
from .ISharepointSite import ISharepointSite

class ISharepointGraphClient(Protocol):
    def sites(self, relative_site_uri:str) -> ISharepointSite:
        """"""
    
    def add_request(self, request:ISharepointGraphRequest):
        """"""