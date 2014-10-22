import locations
import fnmatch
import os
import json
import cjson
import math

_required_fields = ('text', 'created_at', 'user', 'entities', 'id',
                    'coordinates', 'favorite_count', 'favorited',
                    'in_reply_to_status_id',
                    'id_str', 'in_reply_to_screen_name',
                    'in_reply_to_status_id_str', 'in_reply_to_user_id',
                    'in_reply_to_user_id_str', 'lang', 'place',
                    'retweet_count',
                    'retweeted', 'source')

city_coordinates = [coordinates for coordinates in locations.citiesUS]+[coordinates for coordinates in locations.citiesAr]
#print city_coordinates

class FindLocation(object):
    locationTweetsDict = {}
    def classify_city_id(self,geocode):
        '''
        Calculates the euclidian distance between the tweet geocode and cities, to return the value of the clostest city
        '''
        nearest_city_id = city_coordinates[0][0]
        identifier = 0
        minimum = math.sqrt(math.pow(float(city_coordinates[0][1][0]) - float(geocode[0]), 2) +
                        math.pow(float(city_coordinates[0][1][1]) - float(geocode[1]), 2))
        for city in city_coordinates:
          identifier += 1
          temp = math.sqrt(math.pow(float(city[1][0]) - float(geocode[0]), 2) +
                           math.pow(float(city[1][1]) - float(geocode[1]), 2))
          if temp < minimum:
            minimum = temp
            nearest_city_id = city[0]
        return nearest_city_id
    
    def getLocForTweets(self,dr):
        for dirpath, dirs, files in os.walk(dr):
            for eFile in fnmatch.filter(files, '*.txt'):
                fle = dirpath+"/"+eFile
                if os.path.isfile(fle) and fle != None:
                  with open(fle,'r') as myfile:
                    for line in myfile:
                        try:
                            line = cjson.decode(line)
                        except cjson.DecodeError:
                            print "ERROR"+fle
                            continue
                        if "text" in line:
                            '''Filtering tweets from the United States and the Arabian Peninsula'''
                            tweet = {}
                            tweet["text"] = line["text"]
                            tweet["coordinates"] = line["coordinates"]
                            city = self.classify_city_id(tweet["coordinates"]["coordinates"])
                            if city is None:
                                continue
                            if city is not None:
                                if city in self.locationTweetsDict.keys():
                                    self.locationTweetsDict[city].append(dict(tweet))
                                else:
                                    self.locationTweetsDict[city] = []
                                    self.locationTweetsDict[city].append(dict(tweet))
        f = open('locationDict.json','w')
        f.writelines(json.dumps(self.locationTweetsDict))

class Filter(object):
    '''
    Filter tweets according to language and location
    '''
    def process(self,dr):
        for dirpath, dirs, files in os.walk(dr):
            for eFile in fnmatch.filter(files, '*.txt'):
                fle = dirpath+"/"+eFile
                newfile = dirpath+"/"+"new.txt"
                f = open(newfile,"w")
                print fle
                if os.path.isfile(fle) and fle != None:
                  with open(fle,'r') as myfile:
                    for line in myfile:
                        try:
                            line = cjson.decode(line)
                        except cjson.DecodeError:
                            print "ERROR"+fle
                            continue
                        if "text" in line:
                            '''Filtering tweets from the United States and the Arabian Peninsula'''
                            tweet = {}
                            tweet["text"] = line["text"]
                            tweet["coordinates"] = line["coordinates"]
                            if line["lang"] and line["coordinates"]:
                                if line["lang"] == "en" and line["coordinates"]["type"] == "Point":
                                    if float(tweet["coordinates"]["coordinates"][0]) > -157 and float(tweet["coordinates"]["coordinates"][0]) < -66 and float(tweet["coordinates"]["coordinates"][1]) < 64 and float(tweet["coordinates"]["coordinates"][1]) >20:
                                        tweet = json.dumps(tweet)
                                        f.writelines(tweet)
                                        f.write("\n")
                                    elif float(tweet["coordinates"]["coordinates"][0]) > 11 and float(tweet["coordinates"]["coordinates"][0]) < 33 and float(tweet["coordinates"]["coordinates"][1]) < 60 and float(tweet["coordinates"]["coordinates"][1]) >30:
                                        tweet = json.dumps(tweet)
                                        f.writelines(tweet)
                                        f.write("\n")
                os.rename(newfile, fle)