import networkx as nx
import matplotlib.pyplot as plt
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

outfilename="sc_data_T_Map.txt"
infilename="sc_data_T.txt"
idNameMap= "unique_names.txt"
followerCount= "follower_count.txt"
filteredData= "filtered_data.txt"


networkData = {}
followerData = {}

def remove_duplicate_lines():
    print("removing duplicate entries")
    lines_seen = set() # holds lines already seen
    outfile = open(outfilename, "w")
    for line in open(infilename, "r"):
        if line not in lines_seen: # not a duplicate
            outfile.write(line)
            lines_seen.add(line)
    outfile.close()
    print("duplicate entries removed")
    
def uniqueNames():
    print("Finsind unique names")
    name_seen = set() # holds lines already seen
    id_name_map = open(idNameMap, "w")
    for line in open(outfilename, "r"):
        line_names = line.strip().split(" ")
        if line_names[0] not in name_seen: # not a duplicate
            name_seen.add(line_names[0])
            id_name_map.write(line_names[0] + "\n")
        if line_names[1] not in name_seen: # not a duplicate
            name_seen.add(line_names[1])
            id_name_map.write(line_names[1]+ "\n")
    id_name_map.close()
    print("unique name function completed")

def followingNetworkData():
    print("Builidng network map data")
    for line in open(filteredData, "r"):
        line_names = line.strip().split(" ")
        if line_names[0] not in networkData: # not a duplicate
            networkData[line_names[0]] = [line_names[1]]        
        else:
            temp = networkData[line_names[0]]
            temp.append(line_names[1])
            networkData[line_names[0]] = temp
    print("network data process completed")

def outDegreeThrsholdFilter(outLimit):
    #networkData = followingNetworkData()
    #print networkData
    mapTemp = {}
    if networkData is not None:
        for name in networkData:
            if not len(networkData[name]) < outLimit:
                mapTemp[name] = networkData[name]
    return mapTemp


def generateNetwork():
    nodeSet = set()
    G = nx.DiGraph()
    mapTemp = networkData
    #print len(mapTemp)
    for node in mapTemp:
        if node not in nodeSet:
            G.add_node(node)
            follows = mapTemp[node]
            for follow in follows:
                if follow not in nodeSet:
                    G.add_node(follow)
                G.add_edge(node, follow)
    pos= nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True)
    plt.show()


def prepareFollowingData():
    print("Preparing number of followers data")
    id_name_map = open(followerCount, "w")
    for line in open(idNameMap, "r"):
            try:
                user = api.get_user(line.strip())
                followerData[line.strip()] = user.followers_count
                id_name_map.write(line.strip() + " " + str(user.followers_count) +"\n")
            except:
                time.sleep(60 * 15)
                continue
    id_name_map.close()
    print("follower data list completed")


def populateFollwerCountMap():
    for line in open(followerCount, "r"):
        followers = line.split(" ")
        followerData[followers[0]] = int(followers[1])

def findFollowerThreshold():
    temp = []
    for line in open(followerCount, "r"):
        followers = line.split(" ")
        temp.append(int(followers[1]))
    temp.sort()
    size = int(len(temp) * 0.8)
    return temp[size]

def filter_data_with_threshold():
    print("Remove nodes below throshold followers")
    id_name_map = open(filteredData, "w")
    threshold = findFollowerThreshold()
    #print threshold
    #print followerData
    for line in open(outfilename, "r"):
        line_names = line.split(" ")
        if not ((line_names[0] in followerData and followerData[line_names[0]] < threshold) or (line_names[1] in followerData and followerData[line_names[1]] < threshold)):
            id_name_map.write(line)        
    id_name_map.close()
    print("Removed nodes below throshold followers")

remove_duplicate_lines()
uniqueNames()
prepareFollowingData()
filter_data_with_threshold()

followingNetworkData()
#populateFollwerCountMap()
#outDegreeThrsholdFilter(50)
generateNetwork()


