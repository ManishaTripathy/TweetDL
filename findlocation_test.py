import library
import findlocation
import json

class FindLocationTest(object):
  def __init__(self):
      print "Initializing test"
  def run(self):
    tas = library.TweepyAPIs()
    trends = tas.GetTrendsByLocation()[0].get('trends', [])
    terms = [trend.get('name') for trend in trends]
    self.tc.stream(terms)
    
  def filter(self):
    fil = findlocation.Filter()
    dir = "data"
    #fil.process(dir)
    loc = findlocation.FindLocation()
    loc.getLocForTweets(dir)

if __name__ == '__main__':
  tct = FindLocationTest()
  tct.filter()
  