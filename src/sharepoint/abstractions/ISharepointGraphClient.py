from typing import Protocol

from ... import ISharepointGraphRequest, ISharepointSite

class ISharepointGraphClient(Protocol):
    def sites(self, relative_site_uri:str) -> ISharepointSite:
        """"""
    
    def add_request(self, request:ISharepointGraphRequest):
        """"""