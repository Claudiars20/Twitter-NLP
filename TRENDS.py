import tweepy
import pandas as pd




consumer_key = "xj35JjagMNdFSXR83DoxkeEHi"
consumer_secret = "mQurbYtUrdvwVuo3ew3IywWsuX6hVpWoMzXwJaHiiSrnv2SFfj"
access_token = "1404275311492190208-BJ5ufx0Jre0tsSu8kt5LW4wskiLS5D"
access_token_secret = "hyLs6yWTOUf2sEkb0MXWDpepa5XVNmEe2dEosUqIuyDwH"

auth=tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)

api= tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

#Trends de un determinado país
def TopTrends(woeid):
    a = []
    trends = api.trends_place(id = woeid)
    for value in trends:
        for trend in value['trends']:
            a.append(trend['name'])
    return a



Trend=TopTrends(418440)
a = pd.DataFrame(Trend)
a.to_csv("TRENDS/TRENDS.csv")
