from abc import ABC, abstractmethod
from ... import IGraphResponse
from .sharepoint_connection import SharepointConnection

class SharepointGraphClientBase(ABC):
    conn:SharepointConnection
    requests:list[IGraphResponse] = []
    GRAPH_BASE_URI:str = "https://graph.microsoft.com/v1.0/"

    def __init__(self, conn:SharepointConnection):
        self.conn = conn

    @abstractmethod
    def add_request(self, request:IGraphResponse):
        """"""
