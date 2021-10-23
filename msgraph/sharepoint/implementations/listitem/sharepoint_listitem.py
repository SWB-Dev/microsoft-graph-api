from typing import Callable
import requests

from .... import IGraphResponse, IGraphAction, IGraphGetAction, IGraphFilter, ISharepointList
from .... import SharepointGraphClientBase, GraphResponseBase, SharepointListItemBatchAction

class SharepointListItem():

    def __init__(self, id:int, parent:ISharepointList, client:SharepointGraphClientBase):
        self.id = id
        self.parent = parent
        self.client = client
        self.graph_request = GraphResponseBase()
        self.graph_filters:list[IGraphFilter] = []
        self.client.add_request(self.graph_request)

    def filters(self, filter_func:Callable[...,list[IGraphFilter]]) -> IGraphGetAction:
        self.graph_filters = filter_func()
        return self

    def count(self) -> IGraphGetAction:
        """"""
    
    def batch(self, data:list[dict]) -> IGraphAction:
        request_url = self.build_url()
        self.client.requests.remove(self.graph_request)
        return SharepointListItemBatchAction(data, request_url, self.client)
    
    def get(self, url:str = None) -> IGraphResponse:        
        request_url = url or f"{self.client.GRAPH_BASE_URI}{self.build_url()}"
        if not url:
            filter_query = self.build_filter_query()
            request_url += filter_query
        self._get_all(request_url)
        return self.graph_request
    
    def build_url(self) -> str:
        request_url = ''
        if self.parent:
            request_url = self.parent.build_url()
        request_url += "items"
        if self.id:
            request_url += f"/{self.id}"
        return request_url
    
    def build_filter_query(self) -> str:
        filter_query = "&".join([f.compose() for f in self.graph_filters])
        return f"?{filter_query}"

    def _get_all(self, url:str):
        if url is None:
            return
        
        print("GET:",url)
        next_link = '@odata.nextLink'
        r = requests.get(url, headers=self.client.conn.headers)
        self.graph_request.add_response(r)
        resp_json = r.json()

        if next_link in resp_json.keys():
            self._get_all(resp_json[next_link])