import requests
import time

from dataclasses import dataclass

@dataclass
class SharepointConnection():

    tenant_id:str
    client_id:str
    client_secret:str
    refresh_token:str
    scope:str
    expires:int = int(time.time()) - 1
    _headers:dict = None
    auth_resp:dict = None

    @property
    def is_expired(self) -> bool:
        if self.expires < time.time():
            self.auth_resp = None
            self._headers = None
            return True
        return False

    @property
    def headers(self):
        self.establish_connection()
        return self._headers

    def establish_connection(self):
        if self.is_expired:
            self.get_sharepoint_authorization()

    def get_sharepoint_authorization(self):
        auth_url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
        auth_params = {
            'grant_type':'refresh_token',
            'refresh_token':self.refresh_token,
            'client_id':self.client_id,
            'scope':self.scope,
            'client_secret':self.client_secret
        }
        print("Getting Sharepoint access token...")
        auth_resp = requests.post(auth_url, data=auth_params)
        self.auth_resp = auth_resp.json()
        if auth_resp.status_code != 200:
            print("O365 authorization failed.")
            print(self.auth_resp)
            return
        self._handle_auth_response()

    def set_headers(self):
        if self.auth_resp:
            headers = {}
            headers['Content-Type'] = 'application/json'
            headers['Accept'] = 'application/json'
            headers['Authorization'] = f"{self.auth_resp['token_type']} {self.auth_resp['access_token']}"
            self._headers = headers
    
    def _handle_auth_response(self):
        self.expires = int(time.time()) + (self.auth_resp['expires_in'] - 1)
        self.set_headers()