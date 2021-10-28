from typing import Callable
import requests

from .... import IGraphResponse, IGraphFilter, IGraphAction
from ...abstractions.ISharepointDocumentLibrary import ISharepointDocumentLibrary
from ...abstractions.ISharepointList import ISharepointList
from ...utilities.sharepoint_graph_client_base import SharepointGraphClientBase
from ..list.sharepoint_list import SharepointList
from ..documentlibrary.sharepoint_document_library import SharepointDocumentLibrary
from .... import GraphResponseBase

class SharepointSite:

    def __init__(self, site:str, client:SharepointGraphClientBase):
        self.site = site
        self.list = None
        self.library = None
        self.client = client
        self.graph_filters:list[IGraphFilter] = []
        self.graph_request = GraphResponseBase()

    def lists(self, list_name:str = None) -> ISharepointList:
        self.list = SharepointList(self, self.client, list_name)
        return self.list

    def filters(self, filter_func:Callable[...,list[IGraphFilter]]) -> IGraphAction:
        self.graph_filters = filter_func()
        return self

    def documents(self, library_name:str) -> ISharepointDocumentLibrary:
        self.library = SharepointDocumentLibrary(library_name, self, self.client)
        self.client.requests.remove(self.graph_request)
        return self.library

    def get(self, url:str = None) -> IGraphResponse:
        request_url = url or f"{self.client.GRAPH_BASE_URI}{self.build_url()}"
        if not url:
            request_url += self.build_filter_query()
        r = requests.get(request_url, headers=self.client.conn.headers)
        self.graph_request.add_response(r)
        if self.graph_request not in self.client.requests:
            self.client.add_request(self.graph_request)
        return self.graph_request
   
    def build_url(self) -> str:
        request_url = f"sites/root:/sites/{self.site}:/"
        return request_url
    
    def build_filter_query(self) -> str:
        if len(self.graph_filters) < 1:
            return ""
        filter_query = "&".join([f.compose() for f in self.graph_filters])
        return f"?{filter_query}"