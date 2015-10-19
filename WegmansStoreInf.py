#WegmansStoreInf.py

#DESCRPTIONS: 
	#this script is used for collecting data of all the Wegmans Stores in NYS

#INPUTS:	

#VARIABLES:
	#chars_to_remove: 
		#Type: string
		#Content: the chars need to be removed from string 
	#prefix: 

#FUNCTIONS:
	#WegmansListGet():
		#Source: WegmansList.py
		#Usage: Extract 8 elements from the codes roughly extracted and return a list and a dict

#OUTPUTS:

#CREDITS:
	#Chengxi Zhu
	#Department of Geography
	#University at Buffalo, the State University of New York
	#Aug 2015

import urllib.request
import urllib.error
import http.cookiejar
import re
import collections
from WegmansList import *

def WegmansStoreInfGet():

    #########	STEP 0:	#########			
		#Set public variables
		
	#remove 'amp;' to make it reachable
	chars_to_remove='amp;'
	#The prefix 
	prefix='http://www.wegmans.com/webapp/wcs/stores/servlet/'
	#The homepage of Wegmans
	url='http://www.wegmans.com'

	#########	STEP 1:	#########			
		#Visit the homepage of wegmans

	try:
		data=urllib.request.urlopen(url)
	except urllib.error as e:
		print(e)
	MyPage=data.read()
	#print(MyPage)
	unicodePage=MyPage.decode()
	#print(unicodePage)
	Link1=re.findall('<dt class="main-menu-section-title">.*?Store Locator.*?</dt>',unicodePage)
	#http://www.wegmans.com/webapp/wcs/stores/servlet/CategoryDisplay?storeId=10052&amp;catalogId=10002&amp;langId=-1&amp;identifier=CATEGORY_517
	Link2=re.findall('http.*?identifier=CATEGORY_\d*',str(Link1))# convert list to string
	Link2=Link2[0]

	Link3=re.sub(chars_to_remove,'',Link2)
	#Clear the regular expression cache.
	re.purge()

	#########	STEP 2:	#########   
		#Move to the locator page

	url=Link3
	#print(url)
	try:
		data=urllib.request.urlopen(url)
	except urllib.error as e:
		print(e)
	MyPage=data.read()
	unicodePage=MyPage.decode()
	#print(unicodePage)
	# Link1=re.findall('<div id="nav-filter">.*</div>',unicodePage)
	# print(Link1)
	# Link1=re.findall('<a>.*NY.*</a>',str(Link1))
	Link1=re.findall('<a\s.*NY</a>',unicodePage)
	#print(Link1)
	Link2=str(Link1[0])
	Link2=re.sub('"','',Link2)
	Link2=re.sub('>NY</a>','',Link2)
	Link2=re.sub('<a href=','',Link2)
	Link2=re.sub('"','',Link2)
	Link2=re.sub(chars_to_remove,'',Link2)
	#print(Link2)
	Link3=prefix+Link2
	#print(Link3)
	re.purge()

	#########	STEP 3:	#########
		#Read the list of stores in NY

		#########	STEP 3.1:	#########
			#Read the information from 1st Page

	url=Link3
	#print(url)
	try:
		data=urllib.request.urlopen(url)
	except urllib.error as e:
		print(e)
	MyPage=data.read()
	unicodePage=MyPage.decode()
	#re.S	re.DOTALL	make . match newline too.
	Link1=re.findall('<table\sclass="listing">.*</table>',unicodePage,re.S)
	#Collect main part than collect subparts
	Link2=re.findall('<tr>.*</tr>',Link1[0],re.S)
	#print(Link2[0])
	#set a list
	redirectURL=[]
	#Add the Store Information from first page
	for m in re.finditer('<a\shref="StoreDetailView?.*?">\s\d+:\sWegmans\s(\w*\s?-?\w*).*?<table>',Link2[0],re.S):
		redirectURL.append(m.group())

		#########	STEP 3.2:	#########
			#Collect the Link to next page

	Link=re.findall('<a\shref.*?>Next\s&gt;</a>',unicodePage)[0]
	#The extracted part should be:
	#<a href="StoreLocatorView?No=24&forwardto=StoreLocatorView&Ne=10&langId=-1&storeId=10052&identifier=CATEGORY_517&Ns=P_Name&N=157 4294965553&catalogId=10002" alt="Next Page">
	NextPage1=re.findall(';<a\shref.*?alt="Next Page">',Link)[0]
	#print(NextPage1)
	#Remove the additional part
	NextPage2=re.sub(';<a\shref="','',NextPage1)
	NextPage2=re.sub('"\salt="Next Page">','',NextPage2)
	url_nextpage=prefix+NextPage2
	#print(url_nextpage)

	#Here is the TRICKY part:
		#The href is not exact the link we need to visit to next page
		#The following actions will edit them to be the right link

	#Now it is like following:
	#	http://www.wegmans.com/webapp/wcs/stores/servlet/StoreLocatorView?
	#	No=24&forwardto=StoreLocatorView&Ne=10&langId=-1&storeId=10052&
	#	identifier=CATEGORY_517&Ns=P_Name&N=157 4294965553&catalogId=10002
	#It should be reformatted like following:
	#	http://www.wegmans.com/webapp/wcs/stores/servlet/StoreLocatorView?
	#	No=24&forwardto=StoreLocatorView&Ne=10&value=24&langId=-1&
	#	storeId=10052&catalogId=10002&N=157%204294965553&identifier=CATEGORY_517&Ns=P_Name

	#Split the string into two parts by the space between N=157 4294965553
	[url1,url2]=re.split('\s',url_nextpage)
	#Split the url1 string by '&'
	url1parts=re.split('&',url1)	#it would be split into 8 parts
	#Split the url2 string by '&'
	url2parts=re.split('&',url2)	#it would be split into 2 parts
	#'N=157 4294965553'should replace ' '(space) by '%20'
	#then it turns to 'N=157%204294965553'
	urledited=url1parts[7]+'%20'+url2parts[0]
	#change the order
	url=(url1parts[0]+'&'+url1parts[1]+'&'+url1parts[2]+'&'
	+url1parts[3]+'&'+url1parts[4]+'&'+url2parts[1]+'&'+urledited+'&'
	+url1parts[5]+'&'+url1parts[6])#Here url is the Link 

		#########	STEP 3.3:	#########
			#Turn to Next Page and
			#Read the information from 2nd Page

	try:
		data=urllib.request.urlopen(url)
	except urllib.error as e:
		print(e)
	MyPage=data.read()
	unicodePage=MyPage.decode()
	#print(unicodePage)
	Link1=re.findall('<table\sclass="listing">.*</table>',unicodePage,re.S)
	#collect main part than collect subparts
	Link2=re.findall('<tr>.*</tr>',Link1[0],re.S)
	##print(Link2[0])
	#continue the list
	#Add the Store Information from second page
	for m in re.finditer('<a\shref="StoreDetailView?.*?">\s\d+:\sWegmans\s(\w*\s?-?\w*).*?<table>',Link2[0],re.S):
		redirectURL.append(m.group())
	# for i in redirectURL:
	# 	print(i)
	re.purge()

	#########	STEP 4:	#########
		#Extract Information into Dict 'WegmansDict'

	WegmansDict={}
	WegmansStoresList=[]
	l=len(redirectURL)
	for i in range(l):
		#Function from WegmansList.py
		p=WegmansListGet(redirectURL[i])
		WegmansDict[p[0]]=p[1]
		WegmansStoresList.append(p[0])
	WegmansDictOD = collections.OrderedDict(sorted(WegmansDict.items()))
	#WegmansStoreInf(redirectURL[45])
	# for i in range(l):
	# 	print(WegmansStoresList[i] in WegmansDict)
        
	#########	STEP 4:	#########
		#Return Dict 'WegmansDict'

	return WegmansDict
