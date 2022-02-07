

f = open("SmithVideos.txt", "r")
smithString = f.read()

hrefArray = smithString.split('href=')

linkList = []

for indStr in hrefArray:
	justLink = indStr.split(" ")[0].replace('"', '')

	linkList.append(justLink)
	print(justLink)

import pandas as pd

dataFrame = pd.DataFrame()
dataFrame['Links'] = linkList[1:]

dataFrame.to_csv("VideoLinks.csv", index = False)
