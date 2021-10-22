from .... import IGraphResponse, SharepointGraphClientBase, SharepointListItemBatchPost

class SharepointListItemBatchAction:
    
    def __init__(self, data:list[dict], base_uri:str, client:SharepointGraphClientBase):
        self.data = data
        self.base_uri = base_uri
        self.client = client
    
    def post(self, url:str = None) -> IGraphResponse:
        """"""
        action = SharepointListItemBatchPost(self.data, self.base_uri, self.client)
        return action.post(url)