# -*- coding: iso-8859-15 -*-
from Tkinter import *
import BestDressed
import Parties
import Presenters
import Sentiment
import Winners
import json
import pprint

def callback():
	print "click!"

def main():

	master = Tk()

	l = Label(master, text="Golden Globes Project")
	l.grid(row=0, column=0, columnspan=5)

	b = Button(master, text="Find 2013 Awards", command=lambda:Winners.findAwards(2013, False))
	b.grid(row=1, column=0)

	b = Button(master, text="Find 2015 Awards", command=lambda:Winners.findAwards(2015, False))
	b.grid(row=2, column=0)

	b = Button(master, text="Find 2013 Presenters", command=lambda:Presenters.findPresenters(2013, False))
	b.grid(row=1, column=1)

	b = Button(master, text="Find 2015 Presenters", command=lambda:Presenters.findPresenters(2015, False))
	b.grid(row=2, column=1)

	b = Button(master, text="Find 2013 Parties", command=lambda:Parties.parties(2013))
	b.grid(row=1, column=2)

	b = Button(master, text="Find 2015 Parties", command=lambda:Parties.parties(2015))
	b.grid(row=2, column=2)

	b = Button(master, text="Find 2013 Best Dressed", command=lambda:BestDressed.bestDressed(2013))
	b.grid(row=1, column=3)

	b = Button(master, text="Find 2015 Best Dressed", command=lambda:BestDressed.bestDressed(2015))
	b.grid(row=2, column=3)

	b = Button(master, text="2013 Sentiment Analysis", command=lambda:Sentiment.sentimentAnalysis(2013))
	b.grid(row=1, column=4)

	b = Button(master, text="2015 Sentiment Analysis", command=lambda:Sentiment.sentimentAnalysis(2015))
	b.grid(row=2, column=4)

	b = Button(master, text="  \t\t\tRun Basic Tasks\t\t\t   ", command=lambda:doEverything(), default=ACTIVE)
	b.grid(row=3, column=0, columnspan=2)

	master.mainloop()

def writeResults(filename, jsondict):
	encodedjson = json.dumps(jsondict)
	with open(filename, 'w') as out_file:
		out_file.write(encodedjson)

	print "Done writing to file\n"	

def doEverything():
	jsonDict = {}
	Winners.findAwards(2013, jsonDict)
	Presenters.findPresenters(2013, jsonDict)
	
	writeResults("2013results.json", jsonDict)

	jsonDict = {}

	Winners.findAwards(2015, jsonDict)
	Presenters.findPresenters(2015, jsonDict)
	writeResults("2015results.json",jsonDict)

	print "Awaiting another task...\n"

if __name__ == '__main__':
	main()