from ... import IGraphResponse, ISharepointSite
from ... import SharepointGraphClientBase, SharepointSite

class SharepointGraphClient(SharepointGraphClientBase):

    def sites(self, relative_site_uri:str) -> ISharepointSite:
        site = SharepointSite(relative_site_uri, self)
        return site
    
    def add_request(self, request:IGraphResponse):
        self.requests.append(request)