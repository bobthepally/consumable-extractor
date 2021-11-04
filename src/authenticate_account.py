import json

from urllib.parse import urlparse
from urllib.parse import parse_qs
from rauth import OAuth2Service

oauth_file = open("../auth/oauth2_client_info.json")
oauth_info = json.load(oauth_file)

warcraftlogs = OAuth2Service(
    client_id = oauth_info["client_id"],
    client_secret = oauth_info["client_secret"],
    name = "warcraftlogs",
    authorize_url="https://classic.warcraftlogs.com/oauth/authorize",
    access_token_url="https://classic.warcraftlogs.com/oauth/token",
    base_url="https://classic.warcraftlogs.com/"
)

redirect_uri = "http://localhost"
params = {
    'response_type': 'code',
    'redirect_uri': redirect_uri
}

url = warcraftlogs.get_authorize_url(**params)
# parsed_url = urlparse(url)
# code = parse_qs(parsed_url.query)["code"][0]

print(f"URL: {url}")

code_file = open("../auth/user_code.json")
code = json.load(code_file)["code"]

session = warcraftlogs.get_auth_session(data={"code": code, "grant_type": "authorization_code", "redirect_uri": redirect_uri})
