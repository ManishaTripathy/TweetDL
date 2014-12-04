__author__ = 'sthita'


import re
import max_trend_location as obj
import operator

def get_score(tweet):

    #tweet="#job testing #worldcup2014 ajhsdvjahvd jhasd #rip"
    score={}
    tags = re.findall(r"#(\w+)",tweet)
    for tag in tags:
        max= obj.MaxLoc(tag)
        score[tag]=max.get_max_locations()
    loc_scores={}
    loc_count={}
    for tag in score:
        for vals in score[tag]:
            if loc_scores.has_key(vals[0]):
                loc_scores[vals[0]]=loc_scores[vals[0]] + vals[1]
                loc_count[vals[0]]=loc_count[vals[0]]+1
            else:
                loc_scores[vals[0]]=vals[1]
                loc_count[vals[0]]=1
    for loc in loc_scores:
        loc_scores[loc]=float(loc_scores[loc])/loc_count[loc]


    sorted_cities=sorted(loc_scores.items(), key=operator.itemgetter(1),reverse=True)

    return sorted_cities