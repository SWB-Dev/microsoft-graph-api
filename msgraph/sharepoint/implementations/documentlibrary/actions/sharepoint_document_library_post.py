import requests

from ..... import IGraphResponse, SharepointGraphClientBase, GraphResponseBase

class SharepointDocumentLibraryPOST:
    
    def __init__(self, request_url:str, data:dict, client:SharepointGraphClientBase):
        self.request_url = request_url
        self.data = data
        self.client = client
        self.graph_request = GraphResponseBase()
        self.client.add_request(self.graph_request)

    def post(self, url:str = None) -> IGraphResponse:
        self.client.conn.establish_connection()
        request_url = url or self.request_url
        r = requests.post(request_url, headers=self.client.conn.headers, data=self.data)
        self.graph_request.add_response(r)
        return self.graph_request