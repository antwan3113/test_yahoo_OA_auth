import json
import time
import myql
import os
import requests
from yahoo_oauth import OAuth1

currentTime = time.time()
formattedTime = time.strftime("%Z - %Y/%m/%d, %H:%M:%S", time.localtime(currentTime))
league_id = os.environ.get('LEAGUE')
id = "nfl.l.{}".format(league_id)

print league_id
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

for transaction in transactions[:10]:
	type = transaction['type']
	try:
		if type == 'add' or type == 'drop':
			print type
			print "Player: {}".format(transaction['players']['player']['name']['full'])
			print "From: {}".format(transaction['players']['player']['transaction_data']['source_team_name'])
			print "To: {}".format(transaction['players']['player']['transaction_data']['destination_type'])
		else:
			for players in transaction['players']['player']:
				if players['transaction_data']['type'] == "add":
					print players['transaction_data']['type']
					print "Player: {}".format(players['name']['full'])
					print "From: {}".format(players['transaction_data']['source_type'])
					print "To: {}".format(players['transaction_data']['destination_team_name'])
				else:
					print players['transaction_data']['type']
					print "Player: {}".format(players['name']['full'])
					print "From: {}".format(players['transaction_data']['source_team_name'])
					print "To: {}".format(players['transaction_data']['destination_type'])
	except TypeError as e:
		continue
	except KeyError as e:
		continue

# print (json.dumps(transactions, sort_keys=True, indent=4, separators=(',', ': ')))
