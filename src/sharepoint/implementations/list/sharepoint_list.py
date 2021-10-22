from .... import IGraphAction, ISharepointListItem, ISharepointSite, SharepointListItem, SharepointGraphClientBase

class SharepointList():

    def __init__(self, list:str, parent:ISharepointSite, client:SharepointGraphClientBase):
        self.list = list
        self.parent = parent
        self.client = client

    def item(self, id:int) -> ISharepointListItem:
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

    def get(self, url:str = None):
        if url:
            return url
        request_url = self.build_url()
        return request_url

    def get_all(self):
        """TODO: NEEDS IMPLEMENTED"""
    
    def build_url(self) -> str:
        request_url = ''
        if self.parent:
            request_url = self.parent.build_url()
        request_url += f"lists/{self.list}/"
        return request_url