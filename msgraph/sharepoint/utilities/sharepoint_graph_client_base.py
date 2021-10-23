from abc import ABC, abstractmethod
from ... import IGraphResponse, SharepointConnection

class SharepointGraphClientBase(ABC):
    conn:SharepointConnection
    requests:list[IGraphResponse] = []
    GRAPH_BASE_URI:str = "https://graph.microsoft.com/v1.0/"

    def __init__(self, conn:SharepointConnection):
        self.conn = conn

    @abstractmethod
    def add_request(self, request:IGraphResponse):
        """"""
