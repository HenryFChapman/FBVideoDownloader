import pandas as pd 
import os
import selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from zipfile import ZipFile
import shutil
import time
import requests

url = "https://fbdownhd.com/"

with open('folders.txt') as f:
	lines = f.readlines()

#Helper Function to Cause Selenium to Wait to Find the Element Before Downloading
def waitFunction(driver, wait, text):
	try: 
		wait.until(EC.presence_of_element_located((By.XPATH, text)))
	except TimeoutException:
		return False

#Loads download settings
tempDownload = lines[0]

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
prefs = {"profile.default_content_settings.popups": 0,
		"download.default_directory": tempDownload,
		"download.prompt_for_download": False,
		"directory_upgrade": True,
		"safebrowsing.enabled": True}
options.add_experimental_option("prefs", prefs)
options.headless = False
driver = webdriver.Chrome(executable_path=lines[1], options = options)
wait = WebDriverWait(driver, 5)

def inputText(driver, link):

	searchBox = driver.find_element_by_xpath('//*[@id="url"]')
	searchBox.send_keys(link)
	searchButton = driver.find_element_by_xpath('//*[@id="downloadBtn"]')
	searchButton.click()

#Function that waits for the .Zip file to download. Then it unzips the zip file and saves it in a directory
def renameAndUnzip(link):

	while ".crdownload" in os.listdir(tempDownload) or "facebook-video.mp4" not in os.listdir(tempDownload):
		time.sleep(5)
	linkNumber = str(link.split("/")[-2])
	
	#time.sleep(30)
	videos = "Videos\\"
	os.rename(videos+"facebook-video.mp4", videos+linkNumber+".mp4")

def downloadVideo():
	spreadsheet = pd.read_csv("VideoLinks.csv")

	for i, row in spreadsheet.iterrows():
		tempLink = row['Links'].split("/")[-2] + '.mp4'

		if tempLink in os.listdir(tempDownload):
			continue

		if os.path.exists(tempDownload+'facebook-video.mp4'):
			os.remove(tempDownload+'facebook-video.mp4')

		driver.get(url)
		searchBox = driver.find_element_by_css_selector('#url')
		searchBox.send_keys(row['Links'])

		searchButton = driver.find_element_by_xpath('//*[@id="downloadBtn"]')
		searchButton.click()

		successText = '/html/body/div[3]/div/div/div[1]/div/div[2]/a[1]'
		waitFunction(driver, wait, successText)

		time.sleep(30)
		successButton = driver.find_element_by_xpath(successText)
		successButton.click()

		print(row['Links'])
		renameAndUnzip(row['Links'])

downloadVideo()