import tweepy
import time
import Queue

consumer_key = "pDJxB8bzH3eV6ZYthzjgnqXty"
consumer_secret = "60nbLAdK74cDtv3g7CQOl0FTWX1srbRrZeJlW7p9mqMwXaj8av"
access_token = "1066418098893455361-BfoDumlviGj1r8Sbp228tq8pyGxa6n"
access_token_secret = "r3NGctKeeYOchYp7MG9Ja7B9ssjA0HRPsj9bfisH3BAMN"


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
                    with open("gen_data.txt", "a") as myfile:
                        myfile.write(name_next + " " + sname + "\n")
                    if sname not in followerSet:
                        followerSet.add(sname)
                        fcount = user.followers_count
                        with open("follower_data.txt", "a") as followerFile:
                            followerFile.write(sname + " " + fcount + "\n")
                    q.put(sname)
                print len(ids)
    except:
        time.sleep(60*15)
        continue
       
print q
