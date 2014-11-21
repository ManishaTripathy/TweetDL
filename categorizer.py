#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  categorizer.py
#  
#  Copyright 2014 Sreevatsan Vaidyanathan <watson@dragonPC>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
from __future__ import unicode_literals
import requests
import time
import random
import sched
import re
from alchemyapi import AlchemyAPI
alchemyapi = AlchemyAPI()
try:
	import simplejson as json
except ImportError:
	import json
	
class TrendCategorizer():
	""" Categorize Trends obtained from TrendGetter.py """
	
	def __init__ (self):
		""" Class initialiser """
		self.categorizedTrends = {}
		self.trendSummaries = {}
		pass

	def readTrendList (self):
		""" Read the list of trends accumulated  """
		trendList = None
		with open("trends.json",'r')  as fileObject:
			trendList = json.load(fileObject)
		return trendList
	
	def categoryMapper (self,category):
		""" Map obtained category to supercategory """
		categoryDict = {
			"arts_entertainment":"entertainment",
			"business":"finance",
			"sports":"sports",
			"computer_internet":"technology",
			"culture_politics":"politics",
			"gaming":"technology",
			"health":"entertainment",
			"law_crime":"politics",
			"religion":"entertainment",
			"recreation":"entertainment",
			"science_technology":"technology",
			"science_tech":"technology",
			"law":"politics",
			"weather":"entertainment",
			"unknown":str(random.choice(["entertainment","sports"]))
			}
		if category in categoryDict:
			return categoryDict[category]
		else:
			return "entertainment"
		
	def getSummaries (self,trend):
		""" Get Summariies from DuckDuckGo for classification """
		payload = {'q':trend,'format':'json','User-Agent':'newsMashHCC'}
		r = requests.get("http://api.duckduckgo.com",params=payload)
		try:
			response = r.json()
			summary = ""
			if response["Definition"]:
				summary += response["Definition"]+" "
			else:
				for relatedDict in response["RelatedTopics"]:
					if "Topics" not in relatedDict:
						summary += relatedDict["Text"]+" "
			if response["Abstract"]:
				summary += response["Abstract"]+" "
			return summary.encode('ascii','replace')
		except ValueError:
			print ValueError
			return "Error"
	
	def writeToFile (self):
		""" Write categorized Trends and Summaries to JSON files """
		summaryJObject = json.dumps(self.trendSummaries)
		categoryJObject = json.dumps(self.categorizedTrends)
		f = open("catTrends.json",'w').close()
		with open("catTrends.json",'w') as fileP:
			fileP.write(categoryJObject)
		f = open("sumTrends.js",'w').close()
		with open("sumTrends.js",'w') as fileP:
			fileP.write("var SUMMARIES =")
			fileP.write(summaryJObject)	
			fileP.write(";")
		pass
			
	def categorizeTrends (self,trend):
		""" Categorize Trends using generated Summaries """
		trendSummary = self.getSummaries(trend)
		if trendSummary != "Error":
			print trendSummary
			response = alchemyapi.category('text',trendSummary)
			if response['status'] != "ERROR":
				#trendSuperCategory = self.categoryMapper(response['category'])
				self.trendSummaries[trend] = trendSummary
				#self.categorizedTrends[response].append(trend)
				return response
			pass

def main():
	
	t= TrendCategorizer()
	f = open("trends.json")
	catTrends = {}
	trendCity = json.load(f)
	for city in trendCity:
		catTrends[city]={
			"finance":{},
			"technology":{},
			"sports":{},
			"entertainment":{},
			"politics":{}}
		for trendJSON in trendCity[city]:
			#print trendJSON
			tweet_text = trendJSON
			for tweet in trendCity[city][trendJSON]:
				temp = re.sub(r'\W+', ' ', tweet)
				tweet_text = tweet_text +" "+ temp
			tweet_text.encode('ascii','replace')
			print tweet_text
			response = alchemyapi.category('text',tweet_text)
			print response
			if response['status'] != "ERROR":
				trend = str(trendJSON)
				cat = t.categoryMapper(response['category'])
				catTrends[city][cat][trendJSON] = []
				for tweet in trendCity[city][trendJSON]:
					catTrends[city][cat][trendJSON].append(tweet)
	f=open("locTrendCat.json","w")
	f.write(json.dumps(catTrends))
	f.close()
	return 0

if __name__ == '__main__':
	main()

