from typing import Protocol, Optional

from .IGraphResponse import IGraphResponse

class IGraphAction(Protocol):
    def get(self, url:str = None) -> IGraphResponse:
        """"""
    
    def get_all(self):
        """"""

    def post(self, url:Optional[str]) -> IGraphResponse:
        """"""
    
    def patch(self, url:Optional[str]) -> IGraphResponse:
        """"""
    
    def put(self) -> IGraphResponse:
        """"""
    
    def delete(self, url:Optional[str]) -> IGraphResponse:
        """"""   
    
    def build_url(self) -> str:
        """"""

class IGraphPostAction(Protocol):
    def post(self, url:str = None) -> IGraphResponse:
        """"""

class IGraphGetAction(Protocol):
    def get(self, url:str = None) -> IGraphResponse:
        """"""

class IGraphPatchAction(Protocol):
    def patch(self, url:Optional[str]) -> IGraphResponse:
        """"""

class IGraphPutAction(Protocol):
    def put(self) -> IGraphResponse:
        """"""

class IGraphDeleteAction(Protocol):
    def delete(self, url:Optional[str]) -> IGraphResponse:
        """"""  