from requests.models import Response

class SharepointListItemRequest():
    """Implements the ISharepointGraphRequest protocol."""

    def __init__(self):
        self.responses:list[Response] = []
    
    @property
    def request(self):
        return [r.request for r in self.responses]
    
    @property
    def response(self):
        return self.responses
    
    def add_response(self, response:Response):
        self.responses.append(response)
    
    def add_responses(self, responses:list[Response]):
        self.responses.extend(responses)