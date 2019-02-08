import tweepy
import time
import Queue

consumer_key = "JUi8j2tLtVEX90rXK6L5k9OVF"
consumer_secret = "K1tbWaouKe2GrzS8mydmrlLCP8F8d12FYHRpMFxQBtVOkTOQ1s"
access_token = "137293504-I3XbDkYtnMgqMKNPeJywHDPoVvgVRRBxy7FtjmxY"
access_token_secret = "GH1FZhrsB1CUcnI6LSW5FEoD2yEtq3Zm3kBKafLSe0phL"


# Creating the authentication object
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# Setting your access token and secret
auth.set_access_token(access_token, access_token_secret)
# Creating the API object while passing in auth information
api = tweepy.API(auth)

# The Twitter user who we want to get tweets from
name = "sudhirchaudhary"
# Number of tweets to pull
tweetCount = 20

#for user in tweepy.Cursor(api.friends, screen_name="narendramodi").items():
 #   print('friend: ' + user.screen_name)
    
#user = api.get_user(name)
#print user.followers_count

# Calling the user_timeline function with our parameters
#results = api.user_timeline(id=name, count=tweetCount)

# foreach through all tweets pulled
#for tweet in results:
   # printing the text stored inside the tweet object
 #  print tweet.text
  # print tweet.favorite_count
   #print tweet.retweet_count


#file = open('sc_data.txt', 'w')
#file = open('follower_data.txt', 'w')
temp = []
q = Queue.Queue()

q.put("sudhirchaudhary")

followerSet = set()
follower_count= {}

while not q.empty():
    try:
        name_next=q.get()
        #c = tweepy.Cursor(api.friends, screen_name="AsthuSolih").items(200)
        if name_next not in temp:
            temp.append(name_next)
            ids = []
            for page in tweepy.Cursor(api.friends, count = 200, screen_name=name_next).pages():
                ids.extend(page)
                for id in ids:
                    user = api.get_user(user_id=id.id)
                    sname = user.screen_name
                    fcount = user.followers_count
                    if fcount > 10000:
                        #print(fcount)
                        with open("sc_data.txt", "a") as myfile:
                            myfile.write(name_next + " " + sname + "\n")
                        if sname not in followerSet:
                            follower_count[sname] = fcount
                        q.put(sname)
                print len(ids)
                #time.sleep(60)
    except:
        for user in follower_count:
            with open("follower_data.txt", "a") as myfile:
                myfile.write(user + "," + str(follower_count[user]) + "\n")
        time.sleep(60*15)
        follower_count= {}
        continue
print q
