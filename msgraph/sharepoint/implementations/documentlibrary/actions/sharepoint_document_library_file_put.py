import io
import requests

from ..... import IGraphResponse, GraphResponseBase
from ....utilities.sharepoint_graph_client_base import SharepointGraphClientBase

class SharepointDocumentLibraryFilePUT:

    def __init__(self, request_uri:str, stream:io.BufferedIOBase, client:SharepointGraphClientBase):
        self.request_uri = request_uri
        self.stream = stream
        self.client = client
        self.graph_request = GraphResponseBase()
        self.client.add_request(self.graph_request)

    def put(self) -> IGraphResponse:
        self.client.conn.establish_connection()
        request_url = f"{self.client.GRAPH_BASE_URI}{self.request_uri}"
        print(request_url)
        headers = self.client.conn.headers
        headers['content-type'] = 'text/plain'

        r = requests.put(request_url, headers=headers, data=self.stream)

        self.graph_request.add_response(r)
        return self.graph_request