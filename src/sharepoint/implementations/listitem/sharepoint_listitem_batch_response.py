from dataclasses import dataclass

@dataclass
class SharepointListItemBatchResponse():

    response:dict

    __THROTTLE_CODE:int = 429
    __RESPONSES_KEY:str = "responses"

    @property
    def had_response(self):
        return self.__RESPONSES_KEY not in self.response.keys()
    
    @property
    def was_error(self):
        return "error" in self.response.keys()

    @property
    def error_message(self):
        return self.response['error']['message'] or None

    @property
    def was_throttled(self) -> bool:
        if not self.had_response:
            return None
        
        responses = self.response[self.__RESPONSES_KEY]

        for response in responses:
            if response['status'] == self.__THROTTLE_CODE:
                return True
        
        return False
    
    def get_throttled(self) -> list[dict]:
        if self.had_response and not self.was_error:
            responses = self.response[self.__RESPONSES_KEY]
            throttled = [r for r in responses if r['status'] == self.__THROTTLE_CODE]

            return throttled
        return None
    
    def get_throttled_retry_seconds(self) -> int:
        throttled = self.get_throttled()
        throttle_times = [int(x['headers']['Retry-After']) for x in throttled if throttled is not None]
        return max(throttle_times)