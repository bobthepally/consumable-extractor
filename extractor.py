
import json

from wcl_db.wcl_db_wrapper import WCL

def read_credentials(filename):
    """ Read the specified config file for the oauth2 credentials, and returns the result """
    
    oauth_file = open(filename)
    oauth_info = json.load(oauth_file)

    client_id = oauth_info["client_id"]
    client_secret = oauth_info["client_secret"]

    return (client_id, client_secret)

def query_latest_report(db, guild_id):
    """ Queries the db for the latest report from the specified guild and returns the resulting report id """
    
    query = """query {
            reportData {
                reports(guildID: %s, limit: 1) {
                    data {
                        code
                        endTime
                    }
                }
            }
        }
        """ % guild_id
    
    # TODO: handle invalid guild IDs
    response, status_code = db.query(query)
    report_id = str(response["data"]["reportData"]["reports"]["data"][0]["code"])

    return report_id

def query_fight_ids(db, report_id):
    """ Queries the db for all fights from the specified report """

    query = """query {
        reportData {
            report(code: "%s") {
                fights {
                    id,
                    startTime,
                    endTime
                }
            }
        }
    }
    """ % report_id

    # TODO: handle invalid report ids
    response, status_code = db.query(query)
    return response

def query_player_ids(db, report_id):
    """ Queries the db for all players from the specified report """

    query = """query {
        reportData {
            report(code: "%s") {
                masterData{
                    actors(type: "player"){
                        name,
                        id
                    }
                }
            }
        }
    }
    """ % report_id

    response, status_code = db.query(query)
    return response

def main(report_id, guild_id):
    
    client_id, client_secret = read_credentials("auth/oauth2.json")
    wcl = WCL(client_id, client_secret)

    if report_id == "latest":
        report_id = query_latest_report(wcl, guild_id)

    fight_ids = query_fight_ids(wcl, report_id)
    player_ids = query_player_ids(wcl, report_id)
    


if __name__ == "__main__":

    REPORT_ID = "latest"
    GUILD_ID = "490146" #   <Bad on Purpose> on Atiesh

    main(REPORT_ID, GUILD_ID)
