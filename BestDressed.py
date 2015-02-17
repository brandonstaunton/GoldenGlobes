import Winners
import re
import nltk
from nltk import word_tokenize
import urllib2
import time
from bs4 import BeautifulSoup
from pprint import pprint
import random
import webbrowser

urlTextMap = {}

def extractTweets2013():
	return Winners.extractTweets2013()

def extractTweets2015():
	return Winners.extractTweets2015()

def extractRelevantTweets(year):
	print "Removing tweets that don't contain relevant words."
	relevantTweets = []
	#This is the preprocess file by GoldenGolobe.py
	for i, line in enumerate(open("tweets" + str(year) + ".txt", 'r')):
		content = line.lower()
		if content.find("carpet")>=0:
			relevantTweets.append(line)
	# Save specified tweets to file
	with open('redCarpet.txt', 'w') as out_file:
		out_file.write(''.join(relevantTweets))

def getName(list):
	name = {}
	timestamp  = time.time()
	print "start calculating the people name!"
	for line in list:
		namelist = NLTKgetName(line)
		for realName in namelist:
			realName = realName.lower()
			if realName in name:
				name[realName]+=1
			else:
				name[realName]=0
	print "cost " +str(int((time.time()-timestamp)))+"s"
	for k,v in sorted(name.iteritems(), key=lambda d:d[1], reverse = True):
		return k
	return ""

#extract name from twitter content and return the most match one.
def NLTKgetName(text):
	namelist = []
	for sent in nltk.sent_tokenize(text):
		for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
			if hasattr(chunk, "label"):
				if chunk.label() == "PERSON":
					namelist.append(' '.join(c[0] for c in chunk.leaves()))
	return namelist

def FindMostURL(maxium):
	print maxium
	print "start find the twiter contains url and words."
	global urlTextMap
	timestamp  = time.time()
	#urlmap is a map to calculate the times of url that appears.
	urlmap = {}
	#the relatedwords means this is good for the best dressed at redcarpet.
	relatedWords = set(["fashion","dress","dressed","best","gorgeous","great","wonderful","fancy","red","carpet"])
	#the regular expression that match the http 
	reg = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
	for i,line in enumerate(open("redCarpet.txt",'r')):
		urllist = reg.findall(line)
		if len(urllist)>0:
			score = 0
			line = unicode(line,'utf-8')
			for words in word_tokenize((line)): 
				if words in relatedWords:
					score+=1
			if score>0:
				for url in urllist:
					if url in urlmap:
						urlmap[url]+=score
						urlTextMap[url].append(line)
					else:
						urlmap[url]=score
						urlTextMap[url] = [line]

	#the result contains the most metioned url
	result = []
	for k,v in sorted(urlmap.iteritems(), key=lambda d:d[1], reverse = True):
		result.append(k+","+str(v))
		if len(result)>maxium:
			break
	with open('urllist.txt','w') as out_file:
		out_file.write('\n'.join(result))

	print "cost " +str(int((time.time()-timestamp)))+"s"
	return result

def deleteIrrelevant(dict):
	data = re.compile(r'^data:')
	emoji= re.compile(r'abs.twimg')
	spinner = re.compile(r'spinner')
	profile = re.compile(r'profile')
	relative = re.compile(r'^/')
	gif = re.compile(r'.gif')
	cdn = re.compile(r'http://cdn')
	media = re.compile(r'http://media')
	twimg = re.compile(r'https://pbs.twimg.com') #this is hard code here, but more likey to be right.
	result = {}
	for key in dict:
		if key==None:
			continue #special case for some reason.
		v = dict[key]
		if any([media.search(key),cdn.search(key),data.search(key),emoji.search(key),spinner.search(key),profile.search(key),relative.search(key),gif.search(key)]):
			continue
		# this part is hard code.
		if twimg.search(key):
			result[key] = v
	return result


def findThePictureSrc():
	print "start running find picture."
	timestamp  = time.time()
	#referenceMap is used to located the image source and the twitter url.
	referenceMap = {}
	#imgcredibility is used to record the times the img mentioned.
	imgcredibility = {}
	#match the twitter with url.
	global urlTextMap

	for i,line in enumerate(open("urllist.txt",'r')):
		#first part is url the next is count,the second part is the times it mentioned.
		urllist = line.split(",")
		try:
			user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
			hdr = {'User-Agent' : user_agent}
			req = urllib2.Request(urllist[0],headers=hdr)
			html = urllib2.urlopen(req)
		except urllib2.HTTPError,e:
			print "dead link or not connect to internet. broken url:"+urllist[0]
			print e
			continue
		try:
			soup = BeautifulSoup(html)
		except:
			print "invalid data!"
			continue
		for img in soup.find_all('img'):
			src = img.get('src')
			if src in imgcredibility:
				imgcredibility[src]+=1
			else:
				referenceMap[src] = urllist[0]
				imgcredibility[src] =1

	print "cost " +str(int((time.time()-timestamp)))+"s"
	imgcredibility = deleteIrrelevant(imgcredibility)
	result = []
	for k,v in sorted(imgcredibility.iteritems(), key=lambda d:d[1], reverse = True):
		twitterContent=urlTextMap[referenceMap[k]]
		name = getName(twitterContent)
		result.append(k+","+name)
	with open('picturelist.txt','w') as out_file:
		out_file.write('\n'.join(result))

	return result;


def retrivePicture(urllist):
	for item in urllist:
		webpage = item.split(",")[0]
		webbrowser.open_new(webpage)
	#for item in urllist:
	#	fileName = item.split(",")[1]+random.randint(0,10000)+item.split(",")[0].split(".")[1]
	#	for pic in urllist:
	#		data = urllib.urlretrieve(item.split(",")[0],fileName)

def bestDressed(year):
	extractTweets2013() if year == 2013 else extractTweets2015()
	extractRelevantTweets(year)
	FindMostURL(50 if year == 2013 else 10)
	result = findThePictureSrc()
	pprint(result)
	retrivePicture(result)
