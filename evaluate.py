import json

json_actual = open("actual_loc.json")
data_actual = json.load(json_actual)
id_loc_actual={}
for city in data_actual:
    #print city
    for tweet in data_actual[city]:
        #print tweet
        if tweet['id'] is not None:
            print tweet['id']
            id_loc_actual[tweet['id']]=city
json_actual.close()
print id_loc_actual


json_predict = open("predict_loc.json")
data_predict = json.load(json_predict)
id_loc_predict={}
for city in data_predict:
    for tweet in data_predict[city]:
        if tweet['id'] is not None:
            print tweet["id"]
            id_loc_predict[tweet["id"]]=city
total_count=len(id_loc_actual.keys())
total_match=0
for id in id_loc_actual:
    if id in id_loc_predict.keys(): 
        if id_loc_actual[id]==id_loc_predict[id]:
            total_match=total_match+1
accuracy=float(total_match)/total_count

print accuracy
