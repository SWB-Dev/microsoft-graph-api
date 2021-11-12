import json
import requests
import time
from typing import Optional

from .... import IGraphResponse, GraphResponseBase
from .sharepoint_listitem_batch_response import SharepointListItemBatchResponse
from ...utilities.sharepoint_graph_client_base import SharepointGraphClientBase

class SharepointListItemBatchAction:

    BATCH_ITEM_LIMIT:int = 20
    BASE_HEADER:dict = {"Content-Type":"application/json"}
    PAYLOAD_SCHEMA:list[tuple[str,type,str]] = [
        ("id",str,"Batch payload data should include an 'id' key."),
        ("method",str, "Batch payload data should include the 'method' with the HTTP method ('POST')."),
        ("url",str, "Batch payload data should include the 'url' key with the relative URL.  ex: /sites/<site-id>/lists/<list-id>/items"),
        ("body",dict, "Batch payload data should include 'body' key which is a dictionary and key:value pairs for the record data being posted."),
        ("headers",dict, "Batch payload data should include the 'headers' key: {'headers':'application/json'}.  This is different from the header sent for the POST action.")]

    def __init__(self, data:list[dict], base_uri:str, client:SharepointGraphClientBase):
        self.method = ""
        self.data = (d for d in data)
        self.base_uri = base_uri
        self.client = client
        self.graph_request = GraphResponseBase()
        self.client.add_request(self.graph_request)
        self.batch_url = self.client.GRAPH_BASE_URI + "$batch"
    
    def post(self, url:str = None) -> IGraphResponse:
        """Send Batch INSERTS to a SharePoint list."""
        self.method = "POST"
        self._send_data()
        return self.graph_request
    
    def patch(self, url:Optional[str] = None) -> IGraphResponse:
        """Send Batch UPDATES to a SharePoint list."""
        self.method = "PATCH"
        self._send_data()
        return self.graph_request

    def _send_data(self):
        while payload_data:= self._get_batch_payload():
            self._send_batch(payload_data)

    def _send_batch(self, payload_data:dict[str, list[dict]]):
        """Send the Batch to Graph and handle the response if throttled."""
        payload = json.dumps(payload_data)
        r = requests.post(self.batch_url, data=payload, headers=self.client.conn.headers)
        self.graph_request.add_response(r)
        batch_resp = SharepointListItemBatchResponse(r.json())
        if batch_resp.was_throttled:
            retry_seconds = batch_resp.get_throttled_retry_seconds()
            print(f"Batches are being throttled.  Paused for {retry_seconds} seconds.")
            time.sleep(retry_seconds)
            throttled = batch_resp.get_throttled()
            throttled_payload = self._get_throttled_payload(payload_data['requests'], throttled)
            self._send_batch(throttled_payload)

    def _get_throttled_payload(self, orig_payload:list[dict], throttled_responses:list[dict]) -> dict[str, list[dict]]:
        """Gets the original data sent to Graph based on the throttled response ids and returns a new payload."""
        throttled_ids = [r['id'] for r in throttled_responses]
        throttled:list[dict] = [r for r in orig_payload if r['id'] in throttled_ids]
        return {"requests":throttled}

    def _get_batch_payload(self) -> dict[str, list[dict]]:
        """Generates the Batch payload to be sent to Graph."""
        payload:list[dict] = []
        counter = 0
        for d in self.data:
            payload.append(self._build_payload(d))
            counter += 1
            if counter >= self.BATCH_ITEM_LIMIT:
                break        
        return {"requests":payload} if len(payload) > 0 else None
    
    def _build_payload(self, data:dict) -> dict:
        """Builds the payload part for the Batch request."""
        frontloaded = self._frontload_payload(data)
        data_keys = frontloaded.keys()
        for schema in self.PAYLOAD_SCHEMA:
            key = schema[0]
            if key not in data_keys:
                raise KeyError(schema[3])
            if key == "body":
                self._validate_payload_body(data[key])

        if self.method == "PATCH":
            frontloaded['url'] = f"{self.base_uri}{frontloaded['id']}/fields"
            
        return frontloaded
    
    def _validate_payload_body(self, body:dict):
        if not isinstance(body, dict):
            raise TypeError(f"Batch 'body' should be of type: {type(dict).__name__}.")

        body_keys = body.keys()

        if "id" in body_keys:
            raise KeyError("Batch 'body' should not include an 'id' key.")

        if self.method == "POST":
            self._validate_post_body(body)
        
        if self.method == "PATCH":
            self._validate_patch_body(body)

    def _validate_post_body(self, body:dict):
        body_keys = body.keys()

        if not 'fields' in body_keys:
            raise KeyError("Batch 'body' should include the 'fields' key for POST.")
        
        fields = body['fields']

        if not isinstance(fields, dict):
            raise TypeError(f"Batch 'body' 'fields' should be of type: {type(dict).__name__}.")
        
        field_keys = fields.keys()

        if 'id' in field_keys:
            raise KeyError("Batch 'body' 'fields' should not include the key 'id'.")
    
    def _validate_patch_body(self, body:dict):
        body_keys = body.keys()

        if 'fields' in body_keys:
            raise KeyError("Batch 'body' should NOT include the 'fields' key for PATCH.")
        
    def _frontload_payload(self, data:dict) -> dict:
        """Addes or updates required keys for a Graph batch request."""
        data['headers'] = self.BASE_HEADER
        data['method'] = self.method
        data['url'] = self.base_uri
        return data