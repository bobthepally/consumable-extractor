import json

from rauth import OAuth2Service

BASE_URL = "https://classic.warcraftlogs.com"
TOKEN_URL = f"{BASE_URL}/oauth/token"
API_URL = f"{BASE_URL}/api/v2/client"

def main():

    oauth_file = open("auth/oauth2_client_info.json")
    oauth_info = json.load(oauth_file)

    CLIENT_ID = oauth_info["client_id"]
    CLIENT_SECRET = oauth_info["client_secret"]

    warcraftlogs = OAuth2Service(
        client_id = CLIENT_ID,
        client_secret = CLIENT_SECRET,
        name = "warcraftlogs",
        access_token_url=TOKEN_URL,
        base_url=API_URL
    )

    data = {"grant_type": "client_credentials"}

    session = warcraftlogs.get_auth_session(data=data, decoder=json.loads)

    guild_id = "490146" # Bad on Purpose

    query = """query {
        reportData {
            reports(guildID: %s, limit: 1) {
                data {
                    code
                    endTime
                    owner {
                        name
                    }
                    
                    table(dataType: Buffs, startTime: 0, endTime: 1635916495521, hostilityType: Friendlies, killType: Encounters, viewBy: Target)
                }
            }
        }
    }
    """ % (guild_id)

    result = session.post(API_URL, json={'query': query})
    print(result.status_code)
    print(result.text)

main()
