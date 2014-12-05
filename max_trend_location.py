__author__ = 'sthita'

import json
import operator
class MaxLoc:
    def __init__(self, trend_name):
        self.trend_name = trend_name
    def get_max_locations(self):
        print self.trend_name
        json_count = open("trends_count.json")
        data_count = json.load(json_count)
        json_count.close()
        max_city={}
        for city in data_count:
            #print city
            if(data_count[city].has_key(self.trend_name)):
                max_city[city]=data_count[city][self.trend_name]
        sorted_cities=sorted(max_city.items(), key=operator.itemgetter(1),reverse=True)
        #print sorted_cities
        final_list=[]
        count=0
        for value in sorted_cities:
            count=count+1
            final_list.append((value[0],float(0.5)/count))
        #print final_list
        return final_list
