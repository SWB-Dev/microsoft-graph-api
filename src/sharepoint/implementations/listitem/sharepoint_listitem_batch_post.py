import requests
import json
import time

from requests.models import Response

from .... import SharepointGraphClientBase, SharepointListItemRequest, SharepointListItemBatchResponse

class SharepointListItemBatchPost:
    """Implements the IGraphPostAction protocol."""

    BATCH_ITEM_LIMIT:int = 20
    BASE_HEADER:dict = {"Content-Type":"application/json"}
    PAYLOAD_SCHEMA:list[tuple[str,type,str]] = [
        ("id",str,"Batch payload data should include an 'id' key."),
        ("method",str, "Batch payload data should include the 'method' with the HTTP method ('POST')."),
        ("url",str), "Batch payload data should include the 'url' key with the relative URL.  ex: /sites/<site-id>/lists/<list-id>/items",
        ("body",dict, "Batch payload data should include 'body' key which is a dictionary and key:value pairs for the record data being posted."),
        ("headers",dict, "Batch payload data should include the 'headers' key: {'headers':'application/json'}.  This is different from the header sent for the POST action.")]

    def __init__(self, data:list[dict], base_uri:str, client:SharepointGraphClientBase):
        self.data = (d for d in data)
        self.base_uri = base_uri
        self.client = client
        self.throttled_requests = []
        self.graph_request = SharepointListItemRequest()
        self.client.add_request(self.graph_request)
        self.batch_url = self.client.GRAPH_BASE_URI + "$batch"
    
    def post(self, url:str = None):
        """"""
        while payload_data:= self._get_batch_payload():
            self._send_batch(payload_data)

    def _send_batch(self, payload_data:dict[str, list[dict]]):
        """"""
        payload = json.dumps(payload_data)
        r = requests.post(self.batch_url, data=payload, headers=self.client.conn.headers)
        self.graph_request.add_response(r)
        batch_resp = SharepointListItemBatchResponse(r.json())
        if batch_resp.was_throttled():
            retry_seconds = batch_resp.get_throttled_retry_seconds()
            print(f"Batches are being throttled.  Paused for {retry_seconds} seconds.")
            time.sleep(retry_seconds)
            throttled = batch_resp.get_throttled()
            throttled_payload = self._get_throttled_payload(payload_data, throttled)
            self._send_batch(throttled_payload)

    def _get_throttled_payload(self, orig_payload:list[dict], throttled_responses:list[dict]) -> dict[str, list[dict]]:
        """"""
        throttled_ids = [r['id'] for r in throttled_responses]
        throttled:list[dict] = [r for r in orig_payload if r['id'] in throttled_ids]
        return {"requests":throttled}

    def _get_batch_payload(self) -> dict[str, list[dict]]:
        """"""
        payload:list[dict] = []
        counter = 0
        for d in self.data:
            payload.append(self._build_payload(d))
            counter += 1
            if counter >= self.BATCH_ITEM_LIMIT:
                break        
        return {"requests":payload} if len(payload) > 0 else None
    
    def _build_payload(self, data:dict) -> dict:
        frontloaded = self._frontload_payload(data)
        data_keys = frontloaded.keys()
        for schema in self.PAYLOAD_SCHEMA:
            if key := schema[0] not in data_keys:
                raise KeyError(schema[2])
        return frontloaded
    
    def _frontload_payload(self, data:dict) -> dict:
        data['headers'] = self.BASE_HEADER
        data['method'] = "POST"
        data['url'] = self.base_uri
        return data