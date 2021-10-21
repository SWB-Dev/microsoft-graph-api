from typing import Protocol, Optional

class IGraphAction(Protocol):
    def get(self, url:str = None):
        """"""
    
    def get_all(self):
        """"""

    def post(self, url:Optional[str]):
        """"""
    
    def patch(self, url:Optional[str]):
        """"""
    
    def put(self):
        """"""
    
    def delete(self, url:Optional[str]):
        """"""   
    
    def build_url(self) -> str:
        """"""

class IGraphPostAction(Protocol):
    def post(self, url:str = None):
        """"""

class IGraphGetAction(Protocol):
    def get(self, url:str = None):
        """"""

class IGraphPatchAction(Protocol):
    def patch(self, url:Optional[str]):
        """"""

class IGraphPutAction(Protocol):
    def put(self):
        """"""

class IGraphDeleteAction(Protocol):
    def delete(self, url:Optional[str]):
        """"""  