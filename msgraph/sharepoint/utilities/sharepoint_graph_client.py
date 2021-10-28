from ... import IGraphResponse
from ..abstractions.ISharepointSite import ISharepointSite
from .sharepoint_graph_client_base import SharepointGraphClientBase
from ..implementations.site.sharepoint_site import SharepointSite

class SharepointGraphClient(SharepointGraphClientBase):

    def sites(self, relative_site_uri:str) -> ISharepointSite:
        site = SharepointSite(relative_site_uri, self)
        return site
    
    def add_request(self, request:IGraphResponse):
        self.requests.append(request)