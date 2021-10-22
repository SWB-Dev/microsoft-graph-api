import requests

from .... import IGraphResponse, ISharepointList, ISharepointDocumentLibrary
from .... import GraphResponseBase, SharepointGraphClientBase, SharepointList, SharepointDocumentLibrary

class SharepointSite:

    def __init__(self, site:str, client:SharepointGraphClientBase):
        self.site = site
        self.list = None
        self.library = None
        self.client = client
        self.graph_request = GraphResponseBase()
        self.client.add_request(self.graph_request)

    def lists(self, list:str) -> ISharepointList:
        self.list = SharepointList(list, self, self.client)
        self.client.requests.remove(self.graph_request)
        return self.list

    def documents(self, library_name:str) -> ISharepointDocumentLibrary:
        self.library = SharepointDocumentLibrary(library_name, self, self.client)
        self.client.requests.remove(self.graph_request)
        return self.library

    def get(self, url:str = None) -> IGraphResponse:
        if url:
            return url
        request_url = self.build_url()
        r = requests.get(request_url, headers=self.client.conn.headers)
        self.graph_request.add_response(r)
        return self.graph_request
   
    def build_url(self) -> str:
        request_url = f"sites/root:/sites/{self.site}:/"
        return request_url