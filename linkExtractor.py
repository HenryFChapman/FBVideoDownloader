
#This function extracts all links from a chunk of HTML Text
def linkExtractor()

	#Opening the file
	f = open("rawHTML.txt", "r")
	textString = f.read()

	#Splitting It By 'href'
	hrefArray = textString.split('href=')

	#Initializing List and Looping through it
	linkList = []
	for indStr in hrefArray:
		justLink = indStr.split(" ")[0]

		linkList.append(justLink)
		print(justLink)

	#Creating DataFrame and Exporting it
	import pandas as pd

	dataFrame = pd.DataFrame()
	dataFrame['Links'] = linkList

	dataFrame.to_csv("VideoLinks.csv", index = False)
