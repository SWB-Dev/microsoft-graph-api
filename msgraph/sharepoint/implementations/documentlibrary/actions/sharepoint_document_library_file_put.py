import io
import requests
import json

from ..... import IGraphResponse, GraphResponseBase
from ....utilities.sharepoint_graph_client_base import SharepointGraphClientBase

class SharepointDocumentLibraryFilePUT:

    KILOBYTE = 1024
    BYTE_RANGE_SIZE:int = 320 * KILOBYTE
    MAX_BYTE_RANGE = 32 * BYTE_RANGE_SIZE

    def __init__(self, request_uri:str, stream:io.BufferedIOBase, client:SharepointGraphClientBase):
        self.request_uri = request_uri
        self.stream = stream
        self.client = client
        self.graph_request = GraphResponseBase()
        self.client.add_request(self.graph_request)

    def put(self) -> IGraphResponse:
        upload_url = self._open_upload_session(self.request_uri)
        headers = self.client.conn.headers.copy()
        headers['content-type'] = 'text/plain'
        filesize = self._get_filesize()

        start = 0
        end = filesize - 1 if filesize <= self.MAX_BYTE_RANGE - 1 else self.MAX_BYTE_RANGE - 1

        try:
            while data := self.stream.read(self.MAX_BYTE_RANGE):
                data_len = len(data)
                headers['Content-Length'] = f"{data_len}"
                headers['Content-Range'] = f"bytes {start}-{end}/{filesize}"
                r = requests.put(upload_url, headers=headers, data=data)
                if "error" in r.json().keys():
                    error = r.json()['error']
                    raise Exception(error)
                self.graph_request.add_response(r)
                start = end + 1
                end = start + data_len
        except Exception as ex:
            print(ex)
            self._cancel_upload_session(upload_url)

        return self.graph_request
    
    def _get_filesize(self) -> int:
        self.stream.read()
        size = self.stream.tell()
        self.stream.seek(0)
        return size

    def _open_upload_session(self, item_path:str) -> str:
        filename = item_path.split("/")[-1]
        body_data = {
            "items": {
                "@odata.type":"microsoft.graph.driveItemUploadedableProperties",
                "@microsoft.graph.conflictBehavior":"rename",
                "name":filename
            }
        }
        body = json.dumps(body_data)
        request_url = f"{self.client.GRAPH_BASE_URI}{item_path}:/createUploadSession"
        self.client.conn.establish_connection()

        r = requests.post(request_url, headers=self.client.conn.headers, data=body)

        resp = r.json()

        if 'error' in resp.keys():
            error = resp['error']
            raise Exception(error)

        # print(resp['uploadUrl'])
        return resp['uploadUrl']

    def _cancel_upload_session(self, upload_url:str):
        print("Cancelling upload session...")
        r = requests.delete(upload_url, headers=self.client.conn.headers)
        print("Upload session cancelled: {r.status_code}")