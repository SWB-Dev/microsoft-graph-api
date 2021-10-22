from typing import Protocol
from requests.models import Response

class IGraphResponse(Protocol):

    @property
    def request(self):
        """"""
    
    @property
    def response(self):
        """"""
    
    def add_response(self, response:Response):
        """"""
    
    def add_responses(self, responses:list[Response]):
        """"""