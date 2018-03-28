import tweepy
import time
import datetime
import xlsxwriter

consumer_key = "GHlODGEhOO4jxBQDkfjxLKJCS"
consumer_secret = 	"IU7fJAFQsFo1k4l8XZEl5ZERChbz2zVgAWQYHGAyz4pGlKvRX1"
access_key = "954047967404724225-lk9dDdcGzTw9E0bOslcNFRE06lpCHiP"
access_secret = "zF1gBsEmCQrNZIQrwDTFd9cqm09jE49rL6K6BfgWXwzVC"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

usernames = ["elise_chafin",	"xoxo_daria","KamarziTillery","VampKitten629",	"Breka_Nicolee",	"jasmine_twin2",	
"infinite_dom",	"lorenalex98",	"AlanaHadley",	"knownascamie",	"rissascag",	"haseenaaevans",	
"bizzz98",	"Amandakn96",	"AnnaEscobar8",	"michelleeex12",	"JankiPatel98","Cameron_Blake5",	
"AEMcClary11",	"ChrisCGold",	"J_Offschanka11",	"justincooook",	"ryanwesslen",	"willonthe_hill",
	"chrisparish324",	"carsonboykin",	"Johnnyod_17",	"Zyelonkimble14",	"j_mitch_830",	"OverCurved",	"marcusmckee2",
	"DLoveladyBro"]

startDate = datetime.datetime(2018, 2, 1, 0, 0, 0)
endDate =   datetime.datetime(2018, 3, 1, 0, 0, 0)

tweets = []

for user in usernames:
    tmpTweets = api.user_timeline(user,wait_on_rate_limit=True)
    time.sleep(10)
    
    for tweet in tmpTweets:
        if tweet.created_at < endDate and tweet.created_at > startDate:
            tweets.append(tweet)
    
    while (tmpTweets[-1].created_at > startDate):
        print("Last Tweet @", tmpTweets[-1].created_at, " - fetching some more")
        tmpTweets = api.user_timeline(user, max_id = tmpTweets[-1].id)
        for tweet in tmpTweets:
            if tweet.created_at < endDate and tweet.created_at > startDate:
                tweets.append(tweet)

workbook = xlsxwriter.Workbook("tweets_Jan_2018.xlsx")
worksheet = workbook.add_worksheet()
row = 0

worksheet.write_string(row, 0, "Sr No")
worksheet.write_string(row, 1, "User name")
worksheet.write_string(row, 2, "Screen Name")
worksheet.write_string(row, 3, "Description")
worksheet.write_string(row, 4, "Tweet ID")
worksheet.write_string(row, 5, "Created At")
worksheet.write(row, 6, "Tweet Text")
worksheet.write_string(row, 7, "In Reply to")
row = row + 1
 
for tweet in tweets:
    worksheet.write_string(row, 0, str(row))
    worksheet.write_string(row, 1, tweet.user.name.encode('utf-8', errors = 'ignore').decode('utf-8').strip())
    worksheet.write_string(row, 2, str(tweet.user.screen_name.encode('utf-8', errors = 'ignore').strip()))
    worksheet.write_string(row, 3, tweet.user.description.encode('utf-8', errors = 'ignore').decode('utf-8').strip())
    worksheet.write_string(row, 4, str(tweet.id))
    worksheet.write_string(row, 5, str(tweet.created_at))
    if hasattr(tweet,"retweeted_status"):
        worksheet.write(row, 6, str(tweet.retweeted_status.text.encode('utf-8').decode('utf-8').strip()))
    else:
        worksheet.write(row, 6, str(tweet.text.encode('utf-8').decode('utf-8').strip()))
    worksheet.write_string(row, 7, str(tweet.in_reply_to_status_id))
    row += 1
    
workbook.close()