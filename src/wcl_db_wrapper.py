import json

from rauth import OAuth2Service

class WCL:
    
    def __init__(self, client_id, client_secret, initialize=True):
        
        self.base_url = "https://classic.warcraftlogs.com"
        self.token_url = f"{self.base_url}/oauth/token"
        self.api_url = f"{self.base_url}/api/v2/client"

        self.client_id = client_id
        self.client_secret = client_secret

        self.wcl_oauth = OAuth2Service(
            client_id = self.client_id,
            client_secret = self.client_secret,
            name = "warcraftlogs",
            access_token_url=self.token_url,
            base_url=self.api_url
        )

        if initialize:
            self.start_session()

    def start_session(self):
        # Starts an oauth session with WCL

        data = {"grant_type": "client_credentials"}

        self.session = self.wcl_oauth.get_auth_session(data=data, decoder=json.loads)

    def query(self, query_string):
        
        result = self.session.post(self.api_url, json={'query': query_string})
        return result
