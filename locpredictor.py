import max_trend_location as obj
import re
import cjson
import nltk
import os
import math
import json
import locations
import fnmatch
import operator
import get_trend_score

city_coordinates = [coordinates[1] for coordinates in locations.citiesUS]
city_names = [names[0] for names in locations.citiesUS]

def get_all_file_names():
    """Lists of all file names ending with 'endswith' in dir_name and its children Returns: A list of all files in directory tweets ending with '.txt'."""
    for root, _, files in os.walk("data"):
        #print files
        for f in files:
            #print f
            if f.endswith('.txt'):
                yield os.path.join(root, f)

def classify_city_id(geocode):
  '''
  Calculates the euclidian distance between the tweet geocode and cities, to return the value of the clostest city
  '''
  nearest_city_id = 0
  identifier = 0
  minimum = math.sqrt(math.pow(float(city_coordinates[0][0]) - float(geocode[0]), 2) +
                  math.pow(float(city_coordinates[0][1]) - float(geocode[1]), 2))
  for city in city_coordinates[1:]:
    identifier += 1
    temp = math.sqrt(math.pow(float(city[0]) - float(geocode[0]), 2) +
                     math.pow(float(city[1]) - float(geocode[1]), 2))
    if temp < minimum:
      minimum = temp
      nearest_city_id = identifier
  return nearest_city_id

class LocPredictor:
    """Main tweetmapper application."""
    def __init__ (self):
        self.inverse_term_matrix = {}
        self.traing_data = []
        self.target = []
        self.city_vectors = {}
        self.city_vectors_magnitude = {}
    def gettrendscore(self,line):
        '''with open('sample.2014-07-06_00-03.txt','r') as myfile:
            for line in myfile:
                try:
                    line = cjson.decode(line)
                except cjson.DecodeError:
                    print "ERROR"
                    continue'''
        if "text" in line:
            '''Filtering tweets from the United States and the Arabian Peninsula'''
            tweet = {}
            tweet["text"] = line["text"]
            tags = re.findall(r"#(\w+)",line["text"])
            for tag in tags:
                max= obj.MaxLoc(tag)
                #print max.get_max_locations()
            return max.get_max_locations()
                #self.calculate_cosine_similarity(line)
    def calculate_cosine_similarity (self, tweet):  # tweets are in a list.
        """Return the most similar cities for the trend."""
        if not tweet:
            print 'No tweets to classify.'
            return
        query_term_vector = {}
        #tweet = json.loads(tweet)
        for token in re.findall('[a-zA-Z0-9]+', tweet['text']):
            token = self._case_fold(token)
            if not token or token in nltk.corpus.stopwords.words('english'):
                continue
            token = nltk.WordNetLemmatizer().lemmatize(token)
            if query_term_vector.get(token,False):
                query_term_vector[token] += query_term_vector.get(token, 0.0) + 1
            else:
                query_term_vector[token] = 1
                query_magnitude = math.sqrt(
        math.fsum([math.pow(count, 2) for count in query_term_vector.values()]))
    # Calculate cosine scores.
        cosine_scores = {}
        for city, postings in self.city_vectors.iteritems():
            for word in query_term_vector.keys():
                cosine_scores[city] = cosine_scores.get(city, 0.0) + (
                query_term_vector[word] * postings.get(word, 0.0))
                cosine_scores[city] = cosine_scores[city] / (self.city_vectors_magnitude[city] * query_magnitude)
        return sorted(cosine_scores.iteritems(),key=lambda x: x[1],reverse=True)[:50]
    def read_tweet_from_file(self):
        filenames = get_all_file_names()
        #print filenames
        num_files = 0
        for trending_tweet_file in filenames:
            tweets = []
            #print fold
            #print trending_tweet_file
            with open(trending_tweet_file, 'r') as f:
                #print f.readlines()
                tweets = f.readlines()
        for tweet in tweets:
            tweet = json.loads(tweet)
            self._construct_inverse_map(tweet)
        #print tweet
    #print self.inverse_term_matrix
#       with open('%s_cleaned/%s_cleaned.txt' % (fold, trending_tweet_file.rstrip('.txt').lstrip('%s/' % fold)), 'w') as f_new:
#         json.dump(self.inverse_term_matrix, f_new)
#       self.inverse_term_matrix = {}

    def calculate_tfidf(self):
        """Calculate the TF-IDF."""
        for _, posting in self.inverse_term_matrix.iteritems():
            #idf = math.log10(50.0/float(len(posting.keys())))
            idf = 50.0/float(len(posting.keys()))
            for city, tf in posting.iteritems():
                #tfidf = (float(1.0 + math.log10(tf)) * idf)/ (int(city) + 1)
                tfidf = (float(1.0 + tf) * idf)/ (2*int(city) + 1)
                posting[city] = tfidf

    def _case_fold (self, text):
        """Case the given word."""
        return text.lower()

    def _construct_inverse_map (self, tweet):
        """Construct an inverse term dictionary."""
        tweet_city = classify_city_id(tweet['coordinates']['coordinates'])
        for token in re.findall('[a-zA-Z0-9]+', tweet['text']):
            token = self._case_fold(token)
            if not token or token in nltk.corpus.stopwords.words('english'):
                continue
            '''wrd = enchant.Dict("en_US")if not wrd.check(token):continue'''
            token = nltk.WordNetLemmatizer().lemmatize(token)
            postings = self.inverse_term_matrix.get(token, {tweet_city: 0.0})
            postings[tweet_city] = postings.get(tweet_city, 0.0) + 1.0
            self.inverse_term_matrix[token] = postings

    def generate_city_vectors (self):
        for term, postings in self.inverse_term_matrix.iteritems():
            for city, tfidf in postings.iteritems():
                #print city
                #print tfidf
                words = self.city_vectors.get(city, {})
                words[term] = tfidf
                self.city_vectors[city] = words
                self.calculate_city_vectors_magnitude()

    def calculate_city_vectors_magnitude(self):
        for city, vector in self.city_vectors.iteritems():
            self.city_vectors_magnitude[city] = math.sqrt(
            math.fsum([math.pow(tfidf, 2) for tfidf in vector.values()]))
    def run(self):
        self.read_tweet_from_file()
        self.calculate_tfidf()
        with open('tfidf.txt', 'w') as f:
            json.dump(self.inverse_term_matrix, f)
            # return
        self.generate_city_vectors()
        print "generate city vectors"
        #print self.inverse_term_matrix.keys()
        rs = {}
        fle = 'sample.2014-07-06_00-03.txt'
        #print fle
        #fileName[fle]=re.sub('.txt','',eFile)
        #tweets_of_a_trend = []
        f = open("predict_loc.json","w")
        pred_loc = {}
        if os.path.isfile(fle) and fle != None:
            with open(fle,'r') as myfile:
                for line in myfile:
                    #print line
                    #tweets_of_a_trend.append(line)
                    try:
                        line = cjson.decode(line)
                    except cjson.DecodeError:
                        print "ERROR"
                        continue
                    #print line['id']
                    if 'id' in line.keys():
                        #print 'in'
                        rs[line['id']] = {}
                        #rs[line['id']]['tfidf'] = self.calculate_cosine_similarity(line)
                        #rs[line['id']]['tfidf'] = sorted(rs[line['id']]["tfidf"], key=lambda x: x[1],reverse=True)
                        cosine_score = self.calculate_cosine_similarity(line)
                        cosine_score = sorted(cosine_score, key=lambda x: x[1],reverse=True)
                        count = 0
                        val_list = []
                        text = {}
                        for loc in cosine_score:
                            count = count+1
                            #print city_names[loc[0]]
                            val_list.append((city_names[loc[0]],float(0.5)/count))
                        if count==0:
                            continue
                        #rs[line['id']]["trendScore"] = self.gettrendscore(line)
                        #print rs[line['id']]
                        #print val_list
                        val_list_trend = get_trend_score.get_score(line['text'])
                        scores = {}
                        for loc in val_list:
                            if loc[0] not in scores.keys():
                                scores[loc[0]]=0
                            scores[loc[0]]=scores[loc[0]]+float(loc[1])
                        for loc in val_list_trend:
                            if loc[0] not in scores.keys():
                                scores[loc[0]]=0
                            scores[loc[0]]=scores[loc[0]]+float(loc[1])
                        rs[line['id']]=sorted(scores.iteritems(),key=lambda x:x[1],reverse=True)[:1]
                        text["text"]=line["text"]
                        text["id"]=line["id"]
                        text["coordinates"]={}
                        text["coordinates"]["type"]="Point"
                        count = 0
                        for city in city_names:
                            #print city
                            #print 
                            if rs[line['id']][0][0] == city:
                                #print "found a match"
                                text["coordinates"]["coordinates"]=city_coordinates[count]
                            count = count+1
                        #print rs[line['id']][0][0]
                        if rs[line['id']][0][0] is not None:
                            if rs[line['id']][0][0] in pred_loc.keys():
                                pred_loc[rs[line['id']][0][0]].append(text)
                            else:
                                #print "in"
                                #print rs[line['id']][0][0]
                                pred_loc[rs[line['id']][0][0]]=[]
                                pred_loc[rs[line['id']][0][0]].append(text)
                        else:
                            continue
                        '''real_rank = {}
                        #line = json.loads(line)
                        rank = classify_city_id(line["coordinates"]["coordinates"])
                        if real_rank.get(rank,False):
                            real_rank[rank] += 1
                        else:
                            real_rank[rank] = 1
            #rs[eFile]["PureVal"] = real_rank
                        rs[line['id']]["PureVal"]= sorted(real_rank.iteritems(),key=lambda x: x[1],reverse=True)[:50]'''
            #f.writelines(json.dumps(rs))
            print pred_loc
            print pred_loc.keys()
            f.write(json.dumps(pred_loc))
            f.close()


if __name__ == '__main__':
    loc=LocPredictor()
    #loc.gettrendscore()
    loc.run()