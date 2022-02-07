from bs4 import BeautifulSoup
import requests
import pandas as pd
from lxml import etree

def getDates():

	spreadsheet = pd.read_csv("VideoLinks.csv")
	dates = []

	rowLinks = spreadsheet['Links'].tolist()

	for i, row in spreadsheet.iterrows():
		webpage = requests.get(row['Links'])
		html = webpage.text

		try:
			dateCreated = html.split("dateCreated")[1].split(",")[0].split('"')[2]
		except:
			dateCreated = "No Date Found"

		dateCreated.replace('"', '')
		print(dateCreated)

		linkNumber = str(row['Links'].split("/")[-2])
		dates.append(dateCreated)


	linksWithTimes = pd.DataFrame()
	linksWithTimes['Links'] = rowLinks
	linksWithTimes['Date Created'] = dates

	dictionaryOfTimes = linksWithTimes[linksWithTimes['Date Created'] != 'No Date Found']
	dictionaryOfTimes['Date Created'] = pd.to_datetime(dictionaryOfTimes['Date Created'])

	linksWithTimes['Date Created'] = linksWithTimes.merge(dictionaryOfTimes, on = 'Links', how = 'left')

	linksWithTimes.to_csv("LinksWithTimes.csv")

getDates()