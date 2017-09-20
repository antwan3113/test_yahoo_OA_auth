import json
import time
import myql
import requests
from yahoo_oauth import OAuth1

currentTime = time.time()
formattedTime = time.strftime("%Z - %Y/%m/%d, %H:%M:%S", time.localtime(currentTime))
league_id = "nfl.l.646949"

# TODO: this needs to be updated with your actual webhook
#slackUrl = 'put-your-slack-webhook-url-here'

oauth = OAuth1(None, None, from_file="resources/credentials.json")
if not oauth.token_is_valid():
	oauth.refresh_access_token()
yql = myql.MYQL(format='json',oauth=oauth)
resp = yql.raw_query('select * from fantasysports.leagues.standings where league_key="{}"'.format(league_id))
json_response = json.loads(resp.content.decode(resp.encoding))
standings = json_response['query']['results']['league']

resp = yql.raw_query('select * from fantasysports.leagues.transactions where league_key = "{}"'.format(league_id))
json_response = json.loads(resp.content.decode(resp.encoding))
transactions = json_response['query']['results']['league']['transactions']['transaction']

for team in standings['standings']['teams']['team']:
	print json.dumps(team['name'],sort_keys=True, indent=4, separators=(',', ': '))

for transaction in transactions:
	print transaction['type']
	try:
		print transaction['players']['player']['name']
	except TypeError as e:
		continue
	except KeyError as e:
		continue

# print (json.dumps(transactions, sort_keys=True, indent=4, separators=(',', ': ')))
