import requests

from .... import IGraphResponse, IGraphAction, ISharepointListItem, ISharepointSite
from .... import GraphResponseBase, SharepointListItem, SharepointGraphClientBase

class SharepointList():

    def __init__(self, list:str, parent:ISharepointSite, client:SharepointGraphClientBase):
        self.list = list
        self.parent = parent
        self.client = client
        self.graph_request = GraphResponseBase()
        self.client.add_request(self.graph_request)

    def item(self, id:int) -> ISharepointListItem:
        self.client.requests.remove(self.graph_request)
        list_item = SharepointListItem(id, self, self.client)
        return list_item
    
    def items(self) -> ISharepointListItem:
        return self.item(None)

    def columns(self) -> IGraphAction:
        """TODO: NEEDS IMPLEMENTED"""
    
    def content_types(self) -> IGraphAction:
        """TODO: NEEDS IMPLEMENTED"""

    def created_by_user(self) -> IGraphAction:
        """TODO: NEEDS IMPLEMENTED"""

    def last_modified_user(self) -> IGraphAction:
        """TODO: NEEDS IMPLEMENTED"""

    def subscriptions(self) -> IGraphAction:
        """TODO: NEEDS IMPLEMENTED"""

    def get(self, url:str = None) -> IGraphResponse:
        request_url = url or f"{self.client.GRAPH_BASE_URI}{self.build_url()}"
        r = requests.get(request_url, headers=self.client.conn.headers)
        self.graph_request.add_response(r)
        return self.graph_request

    def get_all(self):
        """TODO: NEEDS IMPLEMENTED"""
    
    def build_url(self) -> str:
        request_url = ''
        if self.parent:
            request_url = self.parent.build_url()
        request_url += f"lists/{self.list}/"
        return request_url