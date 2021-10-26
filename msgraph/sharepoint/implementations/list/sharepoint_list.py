import requests
from typing import Callable

from .... import IGraphResponse, IGraphFilter, IGraphAction, ISharepointListItem, ISharepointSite
from .... import GraphResponseBase, SharepointListItem, SharepointGraphClientBase

class SharepointList():

    def __init__(self, parent:ISharepointSite, client:SharepointGraphClientBase, list_name:str = None):
        self.list_name = list_name
        self.parent = parent
        self.client = client
        self.graph_filters:list[IGraphFilter] = []
        self.graph_request = GraphResponseBase()

    def item(self, id:int) -> ISharepointListItem:
        list_item = SharepointListItem(id, self, self.client)
        return list_item
    
    def items(self) -> ISharepointListItem:
        return self.item(None)

    def filters(self, filter_func:Callable[...,list[IGraphFilter]]) -> IGraphAction:
        self.graph_filters = filter_func()
        return self

    def columns(self) -> IGraphAction:
        """TODO: NEEDS IMPLEMENTED"""
        raise NotImplementedError()
    
    def content_types(self) -> IGraphAction:
        """TODO: NEEDS IMPLEMENTED"""
        raise NotImplementedError()

    def created_by_user(self) -> IGraphAction:
        """TODO: NEEDS IMPLEMENTED"""
        raise NotImplementedError()

    def last_modified_user(self) -> IGraphAction:
        """TODO: NEEDS IMPLEMENTED"""
        raise NotImplementedError()

    def subscriptions(self) -> IGraphAction:
        """TODO: NEEDS IMPLEMENTED"""
        raise NotImplementedError()

    def get(self, url:str = None) -> IGraphResponse:
        request_url = url or f"{self.client.GRAPH_BASE_URI}{self.build_url()}"
        if not url:
            request_url += self.build_filter_query()
        r = requests.get(request_url, headers=self.client.conn.headers)
        self.graph_request.add_response(r)
        if self.graph_request not in self.client.requests:
            self.client.add_request(self.graph_request)
        return self.graph_request

    def get_all(self):
        """TODO: NEEDS IMPLEMENTED"""
        raise NotImplementedError()
    
    def build_url(self) -> str:
        request_url = ''
        if self.parent:
            request_url = self.parent.build_url()
        request_url += f"lists/"
        if self.list_name:
            request_url += f"{self.list_name}/"
        return request_url
    
    def build_filter_query(self) -> str:
        if len(self.graph_filters) < 1:
            return ""
        filter_query = "&".join([f.compose() for f in self.graph_filters])
        return f"?{filter_query}"