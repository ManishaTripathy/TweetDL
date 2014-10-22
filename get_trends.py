
import json
import re
import operator


class Trends:

    def __init__(self, file_name,trends_number):
        self.file_name = file_name
        self.trends_number = trends_number

    def get_hash_tags(self):
        JSONLocation = open(self.file_name)
        dataLocation = json.load(JSONLocation)
        f = open("trends.json","w")
        trends = {}

        for city in dataLocation:
            trendsList = {}
            trend_count = {}
            ##print "City---------------------- ",city
            for tweet in dataLocation[city]:
                tweet = tweet["text"]
                tags = re.findall(r"#(\w+)",tweet)
                for tag in tags:
                    if trendsList.has_key(tag.lower()):
                        try:
                            ##print trendsList
                            list_tweets = trendsList[tag.lower()]
                            list_tweets.append(tweet)
                            trendsList[tag.lower()] = list_tweets
                            ##print tag
                        except AttributeError:
                            print "error"


                    else:
                        t_list = []
                        t_list.append(tweet)
                        trendsList[tag.lower()] = t_list
            for trend in trendsList:
                trend_count[trend] = len(trendsList[trend])
            sorted_trends=sorted(trend_count.items(), key=operator.itemgetter(1), reverse=True)
            print city, "---------------"
            final_list = {}
            #print "sorted trend:",len(sorted_trends)
            for value in sorted_trends[:self.trends_number]:
                try:
                    final_list[value[0]] = trendsList[value[0]]
                except KeyError:
                    print "error for",value[0]
            trends[city] = final_list
        json.dump(trends, f)
        JSONLocation.close()


if __name__ == '__main__':
    trend=Trends('locationDict.json',10)
    trend.get_hash_tags()